from accounts import accounts as acc
from accounts import settings
from accounts.models import InitUserTable
from flask import Flask, request, jsonify

app = Flask(__name__)

#Initializing DB
InitUserTable()

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


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


app.add_url_rule("/account/services", \
    view_func=acc.providerCategoryServices, endpoint="Services", methods=["GET"])

"""
app.add_url_rule('/user/<userID>/customerAppointments', \
    view_func=acc.providerCategoryServices, endpoint="CustomerAppointment", methods=["GET"])

app.add_url_rule('/user/<userID>/providerAppointments', \
    view_func=acc.listProviderAppointments, endpoint="providerAppointment", methods=["GET"])
"""
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=8000)

