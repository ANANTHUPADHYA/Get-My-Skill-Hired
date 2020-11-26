import os
import uuid
import boto3
import json
import logging
import requests
from flask import request
from accounts import settings

from warrant import Cognito

from botocore.exceptions import ClientError

from accounts.models import Users, SaveInDB, SerializeUserObj
from accounts.schema import ValidateRegistrationData

from accounts.utils import (
    GetUserPasswordFromAuthHeader, GetResponseObject, \
    GetTokenFromHeader, verify_token, JWTTokenUtil)

from accounts.models import UpdateItem

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.propagate = True

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_REGION = settings.AWS_REGION 
COGNITO_USER_POOL_ID = settings.COGNITO_USER_POOL_ID
COGNITO_APP_CLIENT_ID = settings.COGNITO_APP_CLIENT_ID
S3_URL = settings.S3_URL
S3_BUCKET = settings.S3_BUCKET

# creating aws cognito identity provider client
client = boto3.client("cognito-idp", \
    aws_access_key_id=AWS_ACCESS_KEY_ID, \
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, \
    region_name=AWS_REGION)


s3_client = boto3.client("s3",
   aws_access_key_id=AWS_ACCESS_KEY_ID,
   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def sign_in():
    if request and request.method == "GET":
        resp, err = GetUserPasswordFromAuthHeader(request)
        if err:
            log.error(err)
            res = GetResponseObject(err, 400)
            return res
        
        username, password = resp[0], resp[1]
        
        try:
            user = Cognito(user_pool_id=COGNITO_USER_POOL_ID, \
                client_id=COGNITO_APP_CLIENT_ID, \
                user_pool_region=AWS_REGION, \
                username=username)
            
            user.admin_authenticate(password=password)
            user_rec = user.get_user()
            
            uid = user_rec.sub
            usertype = user_rec._data['custom:usertype']
            
            userObj = Users.get(uid)
            # userObj = Users.get(uid, usertype)

            out = SerializeUserObj(userObj)
            # out["usertype"] = usertype
            data = {
                # "idToken": user.id_token,
                "accessToken": user.access_token,
                # "refreshToken": user.refresh_token,
                "profile": out
            }
            res = GetResponseObject(data, 200, True)
            res.headers['HMS-TOKEN'] = "Bearer " + user.access_token
            # res.set_cookie(settings.COOKIE_NAME , user.access_token)
            return res

        except Exception as e:
            msg = f"Error while authenticating user {str(e)}"
            return  GetResponseObject(msg)
            # return HttpResponseServerError(res)
    else:
        data = f"Invalid request method, method {request.method} not supported !!!"
        return GetResponseObject(data, 405)
        # return HttpResponseBadRequest(res)


def sign_up():
    if request and request.method == "POST":
        resp, err = GetUserPasswordFromAuthHeader(request)
        if err:
            res = GetResponseObject(err, 401)
            log.error(res)
            return res
        
        username, password = resp[0], resp[1]

        if request.data:
            body = json.loads(request.data)
            resp, err = ValidateRegistrationData(body)
            if err:
                res = GetResponseObject(err, 400)
                return res

            try:
                
                body["username"] = username

                # Save user record in Cognito
                user = Cognito(user_pool_id=COGNITO_USER_POOL_ID, client_id=COGNITO_APP_CLIENT_ID, user_pool_region=AWS_REGION)
                user.add_base_attributes(
                    email=username,
                    given_name=body["firstName"],
                    family_name=body["lastName"],
                    phone_number=body["phone"],
                    address=body["address"]
                )
                
                user.add_custom_attributes(
                    usertype=body["userType"],
                    area=body["area"],
                    city=body["city"]
                )

                resp = user.register(username, password)
                # log.info("Cognito response:" + str(resp))

                user.admin_confirm_sign_up()

                body["uuid"] = resp['UserSub']

                # log.info(json.dumps(body, indent=2))
                # saving user record in db
                # filename, err = upload_image(request)
                # if err:
                #     raise Exception(err)

                # body["image"] = "https://" + settings.CLOUD_FRONT_URL + "/" + filename

                SaveInDB(body)

                data = "User registered successfully !!!"
                res = GetResponseObject(data, 200, True)
                return res
                
            except ClientError as e:
                if e.response['Error']['Code'] == 'UsernameExistsException':
                    data = f"{username} username already exists !!!"
                    log.error(data)
                    res = GetResponseObject(data)
                    return res

            except Exception as e:
                user = Cognito( \
                    user_pool_id=COGNITO_USER_POOL_ID, \
                    client_id=COGNITO_APP_CLIENT_ID, \
                    user_pool_region=AWS_REGION, 
                    username=username)

                user.authenticate(password=password)
                resp = client.delete_user(AccessToken=user.access_token)

                log.info(f"Deleting user due to error while signing up: {resp}")
                data = f"Error while registering user: {str(e)}"
                log.error(data)
                res = GetResponseObject(data)
                return res
        else:
            data = f"Empty request body !!!!"
            res = GetResponseObject(data, 400)
            log.error(err)
            return res
    else:
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        log.error(res)
        return res


@verify_token
def sign_out():
    if request and request.method == "GET":
        try:
            auth = request.headers.get('AUTHORIZATION', b'').split()
            response = client.global_sign_out(AccessToken=auth[1])   
            data = "User signed out successfully !!!"
            res = GetResponseObject(data, 200, True)
            return res
        except Exception as e:
            msg = f"Error while signing out user: {str(e)}"
            log.error(msg)
            res = GetResponseObject(msg)
            return res
    else:
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        return res


@verify_token
def delete_user(usertype):
    if request and request.method == "DELETE":
        try:
            auth = request.headers.get('AUTHORIZATION', b'').split()

            j = JWTTokenUtil(auth[1])
            uid = j.get_user_id()

            # Delete user from cognito
            resp = client.delete_user(AccessToken=auth[1])
            log.info(f"User delete from cognito: {uid}\n, {resp}")

            # Delete user data from dynamodb
            result, err = UpdateItem(uid, usertype, delete=True)
            if err:
                raise Exception(err)

            log.info(f"User record delete from DB: {uid}, cognito: {resp}, dynamodb: {result}")

            msg = "User deleted successfully !!!"
            # log.info( msg + "\n" + resp)
            res = GetResponseObject(msg, 200, True)
            return res

        except Exception as e:
            msg = f"Error while deleting user: {str(e)}"
            log.error(msg)
            res = GetResponseObject(msg)
            return res
    else:
        data = f"Invalid request method, method {request.method} not supported !!!"
        res = GetResponseObject(data, 405)
        return res


@verify_token
def update_profile(usertype):
    if request and request.method == "PUT":
        try:

            auth = request.headers.get('AUTHORIZATION', b'').split()
            j = JWTTokenUtil(auth[1])
            uid = j.get_user_id()
            
            body = None
            if request.data:
                body = json.loads(request.data)
                resp, err = ValidateRegistrationData(body, usertype, True)
                if err:
                    res = GetResponseObject(err, 400)
                    return res
            else:
                data = f"Empty request body !!!!"
                res = GetResponseObject(data, 400)
                log.error(err)
                return res

            user = Cognito(
                user_pool_id=COGNITO_USER_POOL_ID, 
                client_id=COGNITO_APP_CLIENT_ID, 
                user_pool_region=AWS_REGION
            )

            out, err = UpdateItem(uid, usertype, body=body, update=True)
            if err:
                raise Exception(err)

            data = "User profile updated successfully !!!"
            res = GetResponseObject(data, 200, True)
            return res

        except Exception as e:
            data = f"Error while updating user profile: {str(e)}"
            log.error(data)
            res = GetResponseObject(data)
            return res            

    else:
        data = f"Invalid request method, method {request.method} not supported !!!"
        return GetResponseObject(data, 405)


def upload_image(request):

    if "profile_image" in request.files:
        file = request.files["profile_image"]
        try:
            s3_client.upload_fileobj(
                file,
                S3_BUCKET,
                file.filename,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": file.content_type
                }
            )
            return file.filename, None

        except Exception as e:
            return file.filename, str(e)
    else:
        return None, "image key name 'profile_image' is not found in header"

    

@verify_token
def upload_profile_image(usertype):
    if request and request.method == "PUT":

        if "profile_image" in request.files:
            file = request.files["profile_image"]
            try:
                if usertype == "consumer":
                    raise Exception("Profile picture upload feature is not available for consumer !!!!")

                s3_client.upload_fileobj(
                    file,
                    S3_BUCKET,
                    file.filename,
                    ExtraArgs={
                        "ACL": "public-read",
                        "ContentType": file.content_type
                    }
                )

                auth = request.headers.get('AUTHORIZATION', b'').split()
                j = JWTTokenUtil(auth[1])
                uid = j.get_user_id()

                resp, err = UpdateItem(uid, usertype, {"image": "https://" + settings.CLOUD_FRONT_URL + "/" + file.filename}, update=True)
                if err:
                    raise Exception(err)
                
                msg = f"User profile image uploaded to s3 and url saved in DB, response: {resp}"
                log.info(msg)
                res = GetResponseObject("User profile image updated !!!", 200, True)
                return res

            except Exception as e:
                msg = f"Error while uploading user profile image : {str(e)}"
                log.error(msg)
                res = GetResponseObject(msg)
                return res            
        else:
            msg = f"No image found"
            log.error(msg)
            res = GetResponseObject(msg)
            return res            

    else:
        data = f"Invalid request method, method {request.method} not supported !!!"
        return GetResponseObject(data, 405)
