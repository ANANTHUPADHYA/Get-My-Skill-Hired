from flask import Flask, request    # import flask
import boto3, os
import uuid
#from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash

#from functions import validatedate, isValidTime

app = Flask(__name__)                      # create an app instance

aws_access_key_id = os.environ.get("DB_AWS_ACCESS_KEY_ID")
if not aws_access_key_id:
    raise ValueError("DB_AWS_ACCESS_KEY_ID not set")

aws_secret_access_key = os.environ.get("DB_AWS_SECRET_ACCESS_KEY")
if not aws_secret_access_key:
    raise ValueError("DB_AWS_SECRET_ACCESS_KEY not set")

db_aws_region = os.environ.get("DB_AWS_REGION")
if not db_aws_region:
    raise ValueError("DB_AWS_REGION not set")

@app.route("/")                            # at the end point /
def hello():                               # call method hello
    return "Hello World!"                  # which returns "hello world"

@app.route("/register/serviceProvider", methods = ['POST'])
def registerServiceProvider():
    dynamodb = boto3.resource('dynamodb', region_name=db_aws_region)

    providerID = uuid.uuid1()
    providerEmail = request.json.get('providerEmail')
    firstName = request.json.get('firstName')
    lastName = request.json.get('lastName')
    phoneNumber = request.json.get('phoneNumber')
    address = request.json.get('address')
    area = request.json.get('area')
    city = request.json.get('city')
    password = generate_password_hash(request.json.get('password'))
    skillsSet = request.json.get('skillsSet')
    daysAvailable  = request.json.get('daysAvailable')
    workingHours = request.json.get('workingHours')
    userType = request.json.get('userType')

    table = dynamodb.Table('Services')
    response = table.put_item(
        Item={
            'providerID': providerID,
            'providerEmail': providerEmail,
            'firstName': firstName,
            'lastName': lastName,
            'phoneNumber': phoneNumber,
            'address': address,
            'area': area,
            'city': city,
            'password': password,
            'skillsSet': skillsSet,
            'daysAvailable': daysAvailable,
            'workingHours': workingHours,
            'userType': userType,
        }
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        data = {
            "success": "true",
            "Message": "Successfully registered.Please login to proceed."
        }
        return data
    else:
        errData = {
            "success": "false",
            "Message": "Unable to register"
        }
        return errData

@app.route("/appointments", methods = ['POST'])
def bookappointment():
    dynamodb = boto3.resource('dynamodb', region_name=db_aws_region)
    print(aws_access_key_id, aws_secret_access_key, db_aws_region)
    appointmentID = uuid.uuid1()
    providerEmail = request.json.get('providerEmail')
    customerEmail = request.json.get('customerEmail')
    date = request.json.get('date')
    time = request.json.get('time')
    serviceType = request.json.get('serviceType')

    table = dynamodb.Table('Appointments')
    response = table.put_item(
        Item={
            'appointmentID': str(appointmentID),
            'providerEmail': providerEmail,
            'customerEmail': customerEmail,
            'date': date,
            'time': time,
            'serviceType': serviceType,
            'appointmentStatus': 'upcoming',
            'rating': None,
            'review': None,
        }
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
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


@app.route("/appointments/<appointmentID>", methods=['PATCH'])
def updateAppointmentStatus(appointmentID):
    dynamodb = boto3.resource('dynamodb', region_name=db_aws_region)

    status = request.json.get('appointmentStatus')

    table = dynamodb.Table('Appointments')
    response = table.update_item(
        Key={
            'appointmentID': appointmentID,
        },
        UpdateExpression="set appointmentStatus=:as",
        ExpressionAttributeValues={
            ':as': status,
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

@app.route("/appointments/<appointmentID>/ratingAndReview", methods = ['PATCH'])
def updateReviewAndRating(appointmentID):
   dynamodb = boto3.resource('dynamodb', region_name=db_aws_region)

   rating = request.json.get('rating')
   review = request.json.get('review')

   table = dynamodb.Table('Appointments')
   response = table.update_item(
       Key={
           'appointmentID': appointmentID,
       },
        UpdateExpression="set rating=:ra, review=:re",
        ExpressionAttributeValues={
            ':ra': rating,
            ':re': review,
        },
        ReturnValues="UPDATED_NEW"
    )

   if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        data = {
            "success": "true",
            "Message": "Successfully rated and reviewed"
        }
        return data
   else:
        errData = {
            "success": "false",
            "Message": "Unable to submit review and rating"
        }
        return errData

if __name__ == "__main__":                 # on running python app.py
    app.run()