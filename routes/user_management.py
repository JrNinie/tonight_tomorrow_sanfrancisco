from flask import Blueprint, request
from tools.decorator_token_required import token_required
from controllers.user_management import (
    create_new_user,
    find_user_by_id,
    modify_user,
    change_password,
    deactivate_user_by_id,
)

user = Blueprint("user", __name__, url_prefix="/users")


@user.route("", methods=["POST"])
def create_user():
    """Create new user
    This allows admin ONLY to create a new user.

    endpoint: /users

    Methods: POST

    Args:
            x-access-token: token genarated after /login
                            and kept in localstorage/cookie
            body: user's info in json (mail, password, first_name,
                  last_name, is_admin, is_activated) except "liked_movie_id"

    Returns:
            message : positive response about action
            OR
            message & error_code : negative response about action
    """
    data = request.get_json()
    return create_new_user(data)


@user.route("/<user_id>", methods=["GET"])
@token_required
def find_user(current_user, user_id):
    """Find user by id

    This allows all users to find himself/herself.
    But admin ONLY could find everyone.

    Endpoint: /users/<user's id>

    Methods: GET

    Args:
            current_user: the user identified by decorator 'token_required'
            x-access-token: token genarated after /login
                            and kept in localstorage/cookie
            user_id: id(uuid) of user you want to find

    Returns:
            user : related info of user wanted
            OR
            message & error_code : negative response about action
    """
    return find_user_by_id(current_user, user_id)


@user.route("/<user_id>", methods=["PUT"])
@token_required
def update_user(current_user, user_id):
    """Update user

    Only admin could modify everyone's info(all columns except password).
    ALL columns (excpet password) are required in the body, even not modifed.

    endpoint: /users/<user_id>

    Methods: PUT

    Args:
            current_user: the user identified by decorator 'token_required'
            x-access-token: token genarated after /login
                            and kept in localstorage/cookie
            body: user's complet info in json
                  (all columns except password required even unchanged)

    Returns:
            message : positive response about action
            OR
            message & error_code : negative response about action
    """

    data = request.get_json()
    return modify_user(current_user, data, user_id)


@user.route("/<user_id>/reset-password", methods=["PUT"])
@token_required
def reset_password(current_user, user_id):
    """Reset password

    Admin could modify everyone's password.
    Ordinary user can modify only his/her password.

    endpoint: /users/<user_id>/reset-password

    Methods: PUT

    Args:
            current_user: the user identified by decorator 'token_required'
            x-access-token: token genarated after /login
                            and kept in localstorage/cookie
            body: user's new password

    Returns:
            message : positive response about action
            OR
            message & error_code : negative response about action
    """

    data = request.get_json()
    return change_password(current_user, data, user_id)


@user.route("/<user_id>/deactivation", methods=["PUT"])
@token_required
def deactivate_user(current_user, user_id):
    """Deactivate user

    This allows admin ONLY to deactivate user by id.

    Endpoint: /users/<user's id>/deactivate

    Methods: PUT

    Args:
            current_user: the user identified by decorator 'token_required'
            x-access-token: token genarated after /login
                            and kept in localstorage/cookie
            user_id: id(uuid) of user you want to deactivate

    Returns:
            message : positive response about action
            OR
            message & error_code : negative response about action
    """

    return deactivate_user_by_id(current_user, user_id)
