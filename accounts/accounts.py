import os
import uuid
import boto3
import json
import logging
import requests
from flask import request
from accounts import settings

from warrant import Cognito

from accounts.models import User, SaveInDB, SerializeUserObj
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

# creating aws cognito identity provider client
client = boto3.client("cognito-idp", \
    aws_access_key_id=AWS_ACCESS_KEY_ID, \
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, \
    region_name=AWS_REGION)


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
            
            userObj = User.get(uid, usertype)

            out = SerializeUserObj(userObj)
            # out["usertype"] = usertype
            data = {
                # "idToken": user.id_token,
                "accessToken": user.access_token,
                # "refreshToken": user.refresh_token,
                "profile": out
            }
            res = GetResponseObject(data, 200)
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
                    email=body["email"],
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

                body["uid"] = resp['UserSub']

                # log.info(json.dumps(body, indent=2))
                # saving user record in db
                SaveInDB(body)

                data = "User registered successfully !!!"
                res = GetResponseObject(data, 200, True)
                return res

            except Exception as e:
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
            res = GetResponseObject(data, 200)
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
            res = GetResponseObject(msg, 200)
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

            data = "User registered successfully !!!"
            res = GetResponseObject(data, 200, True)
            return res

        except Exception as e:
            data = f"Error while registering user: {str(e)}"
            log.error(data)
            res = GetResponseObject(data)
            return res            

    else:
        data = f"Invalid request method, method {request.method} not supported !!!"
        return GetResponseObject(data, 405)
