from botocore.exceptions import ClientError
from flask import Flask, request    # import flask
import boto3, os
import uuid
#from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key

#from functions import validatedate, isValidTime

app = Flask(__name__)                      # create an app instance

aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
if not aws_access_key_id:
    raise ValueError("AWS_ACCESS_KEY_ID not set")

aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
if not aws_secret_access_key:
    raise ValueError("AWS_SECRET_ACCESS_KEY not set")

db_aws_region = os.environ.get("AWS_REGION")
if not db_aws_region:
    raise ValueError("AWS_REGION not set")

@app.route("/")                            # at the end point /
def hello():                               # call method hello
    return "Hello World!"                  # which returns "hello world"

@app.route("/user/<userID>/appointments", methods = ['POST'])
def bookappointment(userID):
    dynamodb = boto3.resource('dynamodb', region_name=db_aws_region)

    appointmentID = uuid.uuid1()
    email = request.json.get('email')
    city = request.json.get('city')
    customerAddress = request.json.get('customerAddress')
    customerEmail = request.json.get('customerEmail')
    customerNumber = request.json.get('customerNumber')
    customerUsername = request.json.get('customerUsername')
    providerEmail = request.json.get('providerEmail')
    date = request.json.get('date')
    day = request.json.get('day')
    rating = None
    review = None
    status = "upcoming"
    time = request.json.get('time')
    serviceType = request.json.get('serviceType')

    appointment = {'appointmentID': str(appointmentID), 'email': email, 'city': city, 'customerAddress': customerAddress, 'customerEmail': customerEmail, 'customerNumber': customerNumber, 'customerUsername': customerUsername, 'providerEmail': providerEmail, 'date': date, 'day': day, 'rating': rating, 'review': review, 'status': status, 'time': time, 'serviceType': serviceType}
    table = dynamodb.Table('Users')
    response = table.update_item(
        Key={
            'uuid': userID,
        },
        UpdateExpression="set appointments = list_append(appointments, :ap)",
        ExpressionAttributeValues={
            ':ap': [appointment],
        },
        ReturnValues="UPDATED_NEW"
    )
    #if result['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Attributes' in result:
    #    return result['Attributes']['some_attr']
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


@app.route("/user/<userID>/appointments/<appointmentID>", methods=['PATCH'])
def updateAppointmentStatus(userID, appointmentID):
    dynamodb = boto3.resource('dynamodb', region_name=db_aws_region)

    status = request.json.get('appointmentStatus')

    table = dynamodb.Table('Users')
    #Get the index of the appointment
    try:
        response = table.get_item(Key={'uuid': userID})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        result = response['Item']

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

@app.route("/user/<userID>/appointments/<appointmentID>/ratingAndReview", methods = ['PATCH'])
def updateReviewAndRating(userID, appointmentID):
   dynamodb = boto3.resource('dynamodb', region_name=db_aws_region)

   rating = request.json.get('rating')
   review = request.json.get('review')

   table = dynamodb.Table('Users')
   # Get the index of the appointment
   try:
       response = table.get_item(Key={'uuid': userID})
   except ClientError as e:
       print(e.response['Error']['Message'])
   else:
       result = response['Item']

   for idx, appointment in enumerate(result["appointments"]):
       if appointment.appointmentID == appointmentID:
        break
   updateExp = "set #app[{}].#rt = :rtVal, #app[{}].#rv = : rvVal".format(idx, idx)
   response = table.update_item(
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