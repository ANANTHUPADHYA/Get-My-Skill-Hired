
from accounts import accounts as acc
from accounts import settings
from accounts.models import InitUserTable
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HireMyService@SJSUFALL2020@CMP281'
app.config['CORS_HEADERS'] = 'Content-Type'

host = settings.HOST_PROTOCOL +  "://" + settings.HOST_NAME + ":" + settings.HOST_PORT
print(host)
cors = CORS(app, resources={r"/account": {"origins": host}})

#Initializing DB
InitUserTable()

app.add_url_rule("/account/signin", \
    view_func=acc.sign_in, endpoint="SignIn", methods=["GET"])

app.add_url_rule("/account/signup", \
    view_func=acc.sign_up, endpoint="SignUp", methods=["POST"])

app.add_url_rule("/account/signout", \
    view_func=acc.sign_out, endpoint="SignOut", methods=["GET"])

app.add_url_rule("/account/delete/<usertype>", \
    view_func=acc.delete_user, endpoint="DeleteUser", methods=["DELETE"])

app.add_url_rule("/account/profile/<usertype>", \
    view_func=acc.update_profile, endpoint="UpdateProfile", methods=["PUT"])

app.add_url_rule("/account/profile/<usertype>/upload", \
    view_func=acc.upload_profile_image, endpoint="UploadProfileImage", methods=["PUT"])

"""
app.add_url_rule("/account/<usertype>/<userID>/services", \
    view_func=acc.providerCategoryServices, endpoint="Services", methods=["GET"])

app.add_url_rule('/user/<userID>/customerAppointments', \
    view_func=acc.providerCategoryServices, endpoint="CustomerAppointment", methods=["GET"])

app.add_url_rule('/user/<userID>/providerAppointments', \
    view_func=acc.listProviderAppointments, endpoint="providerAppointment", methods=["GET"])
"""
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=8000)

