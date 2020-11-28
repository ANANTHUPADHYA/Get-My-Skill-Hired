import os
import uuid
import boto3
import json
import logging
import requests
from flask import Flask,request, Response,jsonify
from flask_cors import cross_origin
from accounts import settings

from warrant import Cognito

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

from accounts.models import Users, SaveInDB, SerializeUserObj
from accounts.schema import ValidateRegistrationData

from accounts.utils import (
    GetUserPasswordFromAuthHeader, GetResponseObject, \
    GetTokenFromHeader, verify_token, JWTTokenUtil)

from accounts.models import UpdateItem
from boto3 import resource
from boto3.dynamodb.conditions import Key


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


# @cross_origin(origin=settings.HOST_NAME, headers=['Content-Type', 'Authorization'])
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
                log.error(res)
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
                body["email"] = username

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

                data = f"Error: {str(e)}"
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

@cross_origin()
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

@cross_origin()
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

@cross_origin()
@verify_token
def update_profile(usertype):
    if request and request.method == "PUT":
        try:

            auth = request.headers.get('AUTHORIZATION', b'').split()
            j = JWTTokenUtil(auth[1])
            uid = j.get_user_id()

            userObj = Users.get(uid)
            if userObj.userType != usertype:
                raise Exception("Please provide correct usertype !!!")
            
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

@cross_origin()
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

    
@cross_origin()
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
    
@verify_token
def providerCategoryServices():

    providerSkillset = request.args.get('skillSet')
    user = "provider"
    dynamodb = resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table("Users")

    scan_kwargs = {
        'FilterExpression': Key('userType').eq(user)}
    response = table.scan(**scan_kwargs)
    items = response['Items']
    res = []
    if len(items) > 0:
        for i, item in enumerate(items):
            skill = item['skillSet']
            appointments=item['appointments']
            review = []
            for appointment in appointments:
                if (appointment['serviceType'])==providerSkillset:
                    review.append(appointment['review'])
            for s in skill:
                if (s['name']) == providerSkillset:
                    res.append({
                        'address': item['address'],
                        'area': item['area'],
                        'city': item['city'],
                        'days': item['days'],
                        'email': item['email'],
                        'firstname': item['firstName'],
                        'lastname': item['lastName'],
                        'phone': item['phone'],
                        'price': str(s['price']),
                        'time': item['time'],
                        'uuid': item['uuid'],
                        'rating':str(item['finalRating']),
                        'image': item['image'],
                        'review': review
                    }
                    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:

        data = {
            "success": "true",
            "data": res
        }
        return data

    else:
        errData = {
            "success": "false",
            "Message": "Unable to fetch data"
        }
        return errData
        




@verify_token
@cross_origin(origin=settings.HOST_NAME, headers=['Content-Type', 'Authorization'])
def bookappointment(userID):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

    appointmentID = uuid.uuid1()
    customerCity = request.json.get('customerCity')
    customerAddress = request.json.get('customerAddress')
    customerEmail = request.json.get('customerEmail')
    customerNumber = request.json.get('customerNumber')
    customerFirstName = request.json.get('customerFirstName')
    customerLastName = request.json.get('customerLastName')
    UUID = request.json.get('uuid')
    providerEmail = request.json.get('providerEmail')
    providerFirstName = request.json.get('providerFirstName')
    providerLastName = request.json.get('providerLastName')
    date = request.json.get('date')
    day = request.json.get('day')
    rating = None
    review = None
    status = "upcoming"
    time = request.json.get('time')
    serviceType = request.json.get('serviceType')

    appointment = {'appointmentID': str(appointmentID), 'uuid': UUID, 'customerCity': customerCity, 'customerAddress': customerAddress, 'customerEmail': customerEmail, 'customerNumber': customerNumber, 'customerFirstName': customerFirstName, 'customerLastName': customerLastName, 'providerFirstName': providerFirstName, 'providerLastName': providerLastName, 'providerEmail': providerEmail, 'date': date, 'day': day, 'rating': rating, 'review': review, 'status': status, 'time': time, 'serviceType': serviceType}
    table = dynamodb.Table('Users')
    providerResponse = table.update_item(
        Key={
            'uuid': userID,
        },
        UpdateExpression="set appointments = list_append(appointments, :ap)",
        ExpressionAttributeValues={
            ':ap': [appointment],
        },
        ReturnValues="UPDATED_NEW"
    )

    appointment = {'appointmentID': str(appointmentID), 'uuid': userID, 'customerCity': customerCity,
                   'customerAddress': customerAddress, 'customerEmail': customerEmail, 'customerNumber': customerNumber,
                   'customerFirstName': customerFirstName, 'customerLastName': customerLastName,
                   'providerFirstName': providerFirstName, 'providerLastName': providerLastName,
                   'providerEmail': providerEmail, 'date': date, 'day': day, 'rating': rating, 'review': review,
                   'status': status, 'time': time, 'serviceType': serviceType}
    table = dynamodb.Table('Users')
    customerResponse = table.update_item(
        Key={
            'uuid': UUID,
        },
        UpdateExpression="set appointments = list_append(appointments, :ap)",
        ExpressionAttributeValues={
            ':ap': [appointment],
        },
        ReturnValues="UPDATED_NEW"
    )

    if providerResponse["ResponseMetadata"]["HTTPStatusCode"] == 200 and customerResponse["ResponseMetadata"]["HTTPStatusCode"]:
        data = {
            "success": "true",
            "Message": "Successfully booked an appointment"
        }
        return data
    else:
        errData = {
            "success": "false",
            "Message": "Unable to book an appointment"
        }
        return errData


@verify_token
@cross_origin(origin=settings.HOST_NAME, headers=['Content-Type', 'Authorization'])
def updateAppointmentStatus(userID, appointmentID):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

    status = request.json.get('status')

    table = dynamodb.Table('Users')
    try:
        response = table.get_item(Key={'uuid': userID})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        result = response['Item']

    #Get the index of the appointment
    for idx, appointment in enumerate(result["appointments"]):
        if appointment["appointmentID"] == appointmentID:
            break
    updateExp = "set #app[{}].#st = :stVal".format(idx)
    response = table.update_item(
        Key={
            'uuid': userID,
        },
        UpdateExpression=updateExp,
        ExpressionAttributeNames={
            '#app': 'appointments',
            '#st': 'status'
        },
        ExpressionAttributeValues={
            ':stVal': status,
        },
        ReturnValues="UPDATED_NEW"
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        data = {
            "success": "true",
            "Message": "Successfully updated appointment status"
        }
        return data
    else:
        errData = {
            "success": "false",
            "Message": "Unable to update appointment status"
        }
        return errData


@verify_token
@cross_origin(origin=settings.HOST_NAME, headers=['Content-Type', 'Authorization'])
def updateReviewAndRating(userID, appointmentID):
   dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

   rating = request.json.get('rating')
   review = request.json.get('review')

   table = dynamodb.Table('Users')
   try:
       response = table.get_item(Key={'uuid': userID})
   except ClientError as e:
       print(e.response['Error']['Message'])
   else:
       result = response['Item']

   # Get the index of the appointment
   for idx, appointment in enumerate(result["appointments"]):
       if appointment["appointmentID"] == appointmentID:
           UUID = appointment["uuid"]
           break
   updateExp = "set #app[{}].#rt = :rtVal, #app[{}].#rv = :rvVal".format(idx, idx)

   providerResponse = table.update_item(
       Key={
           'uuid': userID,
       },
        UpdateExpression=updateExp,
        ExpressionAttributeNames={
            '#app': 'appointments',
            '#rt': 'rating',
            '#rv': 'review'
        },
        ExpressionAttributeValues={
            ':rtVal': rating,
            ':rvVal': review
        },
        ReturnValues="UPDATED_NEW"
    )

   customerResponse = table.update_item(
       Key={
           'uuid': UUID,
       },
       UpdateExpression=updateExp,
       ExpressionAttributeNames={
           '#app': 'appointments',
           '#rt': 'rating',
           '#rv': 'review'
       },
       ExpressionAttributeValues={
           ':rtVal': rating,
           ':rvVal': review
       },
       ReturnValues="UPDATED_NEW"
   )

   if providerResponse["ResponseMetadata"]["HTTPStatusCode"] == 200 and customerResponse["ResponseMetadata"]["HTTPStatusCode"] == 200:
       #Update final rating
       finalrating = 0.0
       count = 0

       try:
           response = table.get_item(Key={'uuid': userID})
       except ClientError as e:
           print(e.response['Error']['Message'])
       else:
           result = response['Item']

       for _, appointment in enumerate(result["appointments"]):
           if appointment["rating"] is not None:
               count = count + 1
               finalrating = finalrating + float(appointment["rating"])

       if count != 0:
           finalrating = finalrating/count

       finalrating = str(finalrating)

       updatefinalRatingExp = "set #fr = :frVal"
       updatedRes = table.update_item(
           Key={
               'uuid': userID,
           },
           UpdateExpression=updatefinalRatingExp,
           ExpressionAttributeNames={
               '#fr': 'finalRating'
           },
           ExpressionAttributeValues={
               ':frVal': finalrating,
           },
           ReturnValues="UPDATED_NEW"
       )
       if updatedRes["ResponseMetadata"]["HTTPStatusCode"] == 200:
            updatedmessage = {
                "success": "true",
                "Message": "Successfully rated and reviewed the appointment. Also updated the final rating of the provider"
            }
            return updatedmessage
       else:
           data = {
               "success": "true",
               "Message": "Successfully rated and reviewed the appointment. Failed to update the final rating"
           }
           return data
   else:
        errData = {
            "success": "false",
            "Message": "Unable to submit review and rating"
        }
        return errData
  

@verify_token
@cross_origin(origin=settings.HOST_NAME, headers=['Content-Type', 'Authorization'])
def listCustomerAppointments(userID):
   Cutomeruuid=userID
   if Cutomeruuid:
       dynamodb_resource = resource('dynamodb', region_name=AWS_REGION)
       table = dynamodb_resource.Table('Users')
       response = table.query(KeyConditionExpression=Key('uuid').eq(Cutomeruuid))
       items = response['Items']

       if len(items) > 0:
           appointments = items[0]['appointments']

       if response["ResponseMetadata"]["HTTPStatusCode"] == 200:

           data = {
               "success": "true",
               "data": appointments
           }
           return data

       else:
           errData = {
               "success": "false",
               "Message": "Unable to fetch data"
           }
           return errData
    
    
    
@verify_token
@cross_origin(origin=settings.HOST_NAME, headers=['Content-Type', 'Authorization'])
def listProviderAppointments(userID):
   providerUuid=userID

   if providerUuid:
       dynamodb_resource = resource('dynamodb', region_name=AWS_REGION)
       table = dynamodb_resource.Table('Users')
       response = table.query(KeyConditionExpression=Key('uuid').eq (providerUuid))
       items = response['Items']
       if len(items) > 0:
           appointments = items[0]['appointments']

       if response["ResponseMetadata"]["HTTPStatusCode"] == 200:

           data = {
               "success": "true",
               "data": appointments
           }
           return data

       else:
           errData = {
               "success": "false",
               "Message": "Unable to fetch data"
           }
           return errData
        
