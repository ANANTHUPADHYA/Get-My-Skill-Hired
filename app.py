from flask import Flask, request, session, Response, jsonify  # import flask
import boto3, os
from boto3 import resource
import uuid
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key

# from functions import validatedate, isValidTime

app = Flask(__name__)  # create an app instance



@app.route("/")  # at the end point /
def hello():  # call method hello
    return "Hello World!"  # which returns "hello world"


@app.route('/service')
def providerCategoryServices():
    s = 'provider'
    providerSkillset= request.args.get('skillSet')

    if s:
        dynamodb = resource('dynamodb', region_name=db_aws_region)
        table = dynamodb.Table("Users")

        scan_kwargs = {
            'FilterExpression': Key('userType').eq(s)}

        response = table.scan(**scan_kwargs)
        items = response['Items']

        print (items[0]['area'])
        if len(items) > 0:
            res = []

            for i, item in enumerate(items):
                skill=item['skillSet']
                print(skill)
                for s in skill:
                    print(s['name'])
                    if (s['name'])==providerSkillset:
                        print("true")
                        res.append({

                        'address':item['address'],
                        'area': item['area'],
                        'city': item['city'],
                        'days': item['days'],
                        'email': item['email'],
                        'firstname':item['firstName'],
                        'lastname': item['lastName'],
                        'phone': item['phone'],
                        'price': s['price'],
                        'time': item['time'],
                        'uuid': item['uuid'],
                        'rating' : item['finalRating'],
                        'image': item['image']
                }
                )
            print(res)

        return jsonify(res)


@app.route('/ProviderAppointments')
def listProviderAppointments():

   Provideruuid= request.args.get('uuid')

   if Provideruuid:
       dynamodb_resource = resource('dynamodb', region_name=db_aws_region)
       table = dynamodb_resource.Table('Users')
       response = table.query(KeyConditionExpression=Key('uuid').eq (Provideruuid))
       items = response['Items']


       if len(items) > 0:
           appointments = items[0]['appointments']
           return(jsonify(appointments[0]))

       else:
           status="error"
           return jsonify({"status": "get failed", "error": items}), status
   else:
       return ("uuid not found")


""""
           res=[]
           for i in range (len(items)):
               item=items[i]
               print(i)
               appointments = item['appointment']
               print(appointments)
               
            

                   for appointment in appointments:
                       for a in appointment:
                           print("yes")
                           print(len(appointments))

                           res.append({

                                   'appointmentID': a['appointmentID'],
                                   'city': a['city'],
                                   'day': a['day'],
                                   'date': a['date'],
                                   'customerEmail': a['customerEmail'],
                                   'serviceType': a["serviceType"],
                                   'customerNumber' :a['customerNumber'],
                                   'customerAddress ': a['customerAddress'],
                                   "customerUsername": a["customerUsername"],
                                   'status': a['status'],
                                   'time': a['time'],
                                   'rating': a['rating'],
                                   'review': a['review']
                               })
           print(res)

       return jsonify(res)

"""


@app.route('/CustomerAppointments')
def listCustomerAppointments():

   Cutomeruuid= request.args.get('uuid')
   #CustomerEmail="yes"
   if Cutomeruuid:
       dynamodb_resource = resource('dynamodb', region_name=db_aws_region)
       table = dynamodb_resource.Table('Users')
       response = table.query(KeyConditionExpression=Key('uuid').eq(Cutomeruuid))
       items = response['Items']
       print(items)

       if len(items) > 0:
           appointments = items[0]['appointments']
           return(jsonify(appointments[0]))

""""
       if len(items) > 0:
           res=[]
           for i, item in enumerate(items):
               appointments = item['appointments']
               print(appointments)
               for a in appointments:
                   print(a)
                   print(a[0]['status'])
                   res.append({
            'appointmentID': a[0]['appointmentID'],
           'day': a[0]['day'],
           'date': a[0]['date'],
           'providerEmail': a[0]['providerEmail'],
           'serviceType': a[0]["serviceType"],
           'userName': a[0]['UserName'],
           'ProviderPhone': a[0]['providerNumber'],
           'status': a[0]['status'],
           'time': a[0]['time'],
           'rating': a[0]['rating'],
           'review': a[0]['review']
       })
                   print("y")
       print(res)

       return jsonify(res)
       
       """


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
