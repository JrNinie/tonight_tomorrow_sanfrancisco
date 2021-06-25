from flask import request, Blueprint, current_app
from controllers.authentication import verify_login


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login():
    """User's login
    This allows all users to login and get a confidential token as response.

    Endpint: /login

    Methods: GET

    Params:
            Authorization: basic auth with username(sigfox mail) and password

    Returns:
            token: (if mail & password correct) confidential token
            OR
            message & Error_Code : (if mail/password incorrect)
                                   negative response about action
    """
    auth = request.authorization
    secret_key = current_app.config["SECRET_KEY"]
    return verify_login(auth, secret_key)
