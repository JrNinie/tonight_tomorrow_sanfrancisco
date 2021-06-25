from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
import re
from models.user import User
from models import db
from exceptions.errors import PermissionError, InputError, NotFoundError, DatabaseError
from log.my_logger import get_logger
from tools.user import is_uuid, verify_type_integrity_of_data, verify_data_form

logger = get_logger()


def create_new_user(current_user, data):
    # Data form check (dict send in json)
    verify_data_form(data)

    # Data type & integrity check
    template = {
        "first_name": str,
        "password": str,
        "is_activated": bool,
        "is_admin": bool,
        "last_name": str,
        "mail": str,
    }
    verify_type_integrity_of_data(template, data)

    # Prepare data
    mail = data["mail"].lower()
    # Mail validation
    left = "^[A-Za-z0-9]+([_\-\.][A-Za-z0-9]+)*"
    right = "([A-Za-z0-9\-]+\.)+[A-Za-z]{2,6}$"
    regex = rf"{left}@{right}"
    if not re.search(regex, mail):
        logger.error(f"{mail} is not a valid email address.")
        raise InputError(message="Only a valid email address is accepted.")
    first_name = data["first_name"].capitalize()
    last_name = data["last_name"].capitalize()
    is_admin = data["is_admin"]
    is_activated = data["is_activated"]
    password = data["password"]
    # Password check
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{6,20}$"
    if not re.match(re.compile(reg), password):
        logger.error(f"{mail}'s password is unauthorized")
        raise InputError(message="This password is unauthorized.")
    # Encrypt password
    hashed_password = generate_password_hash(password, method="sha256")

    # Save in database
    try:
        new_user = User(
            mail=mail,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            is_activated=is_activated,
        )
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session().rollback()
        message = "Database error du to the wrong input."
        # Unique key violation error
        if str(e).find("psycopg2.errors.UniqueViolation") != -1:
            message = f"The user {mail} exists already."
        logger.error(f"{message}, details: {e}")
        raise InputError(message=message)
    except Exception as e:
        db.session().rollback()
        logger.critical(
            f"There are errors when create new user in database, details: {e}"
        )
        raise DatabaseError(
            message="There are errors when create new user in database."
        )

    logger.info(f"User({mail}) has been created successfully.")
    return {"message": f"New user ({mail}) created successfully"}, 201


def find_user_by_id(current_user, user_id):
    if not current_user.is_admin:
        if not str(current_user.id) == user_id:
            logger.error(
                f"No admin user({current_user.id}) tried to \
            find user({user_id})."
            )
            raise PermissionError(
                message="It's not authorized to perform this operation"
            )

    # Valid uuid check
    if not is_uuid(user_id):
        logger.error(f"The id({user_id}) is not a valid uuid.")
        raise InputError(message="The user's id must be a valid uuid.")

    try:
        user = User.query.filter_by(id=user_id).first()
    except Exception as e:
        logger.critical(f"Failed to query user from database, details: {e}")
        raise DatabaseError(message="There are errors when find user in database.")

    if not user:
        logger.error(f"This user({user_id}) doesn't exist")
        raise NotFoundError(message="This user doesn't exist")

    if not current_user.is_admin:
        logger.info(
            "User info(without password, is_activated) has been\
         displayed successfully."
        )
        return user.to_dict("password", "is_activated")

    logger.info("User info(without password) has been displayed successfully.")
    return user.to_dict("password")


def modify_user(current_user, data, user_id):

    if not current_user.is_admin:
        logger.error(
            f"User no admin {current_user.id} is not allowed to \
        update user's info."
        )
        raise PermissionError(message="Only admin can perform this operation")

    # Data form check (dict send in json)
    verify_data_form(data)

    # Data type & integrity check
    template = {
        "mail": str,
        "first_name": str,
        "last_name": str,
        "is_activated": bool,
        "is_admin": bool,
    }
    verify_type_integrity_of_data(template, data)
    # Valid uuid check
    if not is_uuid(user_id):
        logger.error(f"The id({user_id}) is not a valid uuid.")
        raise InputError(message="The user's id must be a valid uuid.")

    # Find & modify user
    id = user_id
    mail = data["mail"].lower()
    # Mail validation
    left = "^[A-Za-z0-9]+([_\-\.][A-Za-z0-9]+)*"
    right = "([A-Za-z0-9\-]+\.)+[A-Za-z]{2,6}$"
    regex = rf"{left}@{right}"
    if not re.search(regex, mail):
        logger.error(f"{mail} is not a valid sigfox email address.")
        raise InputError(message="Only a valid sigfox email address is accepted.")
    first_name = data["first_name"].capitalize()
    last_name = data["last_name"].capitalize()
    is_admin = data["is_admin"]
    is_activated = data["is_activated"]
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            logger.error(f"User({id}) doesn't exist.")
            raise NotFoundError(message="This user doesn't exist")
        user.mail = mail
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = is_admin
        user.is_activated = is_activated
        db.session.merge(user)
        db.session.commit()
    except Exception as e:
        logger.critical(f"There are errors when update user({id}), details: {e}")
        raise DatabaseError(message="There are errors when update user in database.")

    logger.info(f"User({id}) has been updated successfully.")
    return {"message": "User's info has been updated successfully"}


def change_password(current_user, data, user_id):

    # Data form check (dict send in json)
    verify_data_form(data)

    # Data type & integrity check
    template = {"password": str}
    verify_type_integrity_of_data(template, data)
    # Valid uuid check
    if not is_uuid(user_id):
        logger.error(f"The id({user_id}) is not a valid uuid.")
        raise InputError(message="The user's id must be a valid uuid.")
    # Valid password check
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{6,20}$"
    if not re.match(re.compile(reg), data["password"]):
        logger.error(f"User({data['id']})'s password is unauthorized")
        raise InputError(message="This password is unauthorized.")

    # Permission check
    # Only admin can change for other user
    if not current_user.is_admin and not str(current_user.id) == user_id:
        logger.error(f"User no admin ({current_user.id}) can not change other's pwd.")
        raise PermissionError(
            message="You are not authorized to perform this operation."
        )

    id = user_id
    password = data["password"]
    password_hashed = generate_password_hash(password, method="sha256")
    # Find user & modify password
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            logger.error(f"User({id}) doesn't exist.")
            raise NotFoundError(message="This user doesn't exist.")

        user.password = password_hashed
        db.session.merge(user)
        db.session.commit()
    except Exception as e:
        logger.critical(
            f"Failed to update user({id})'s password in database, details: {e}"
        )
        raise DatabaseError(message="There are errors when find user in db.")

    logger.info(f"Password of user({id}) has been changed successfully.")
    return {"message": "user's info has been changed successfully"}


def deactivate_user_by_id(current_user, user_id):

    if not current_user.is_admin:
        logger.error(f"User {current_user.id} (not admin) tried to deactivate user.")
        raise PermissionError(message="Only admin can deactivate user.")

    if not is_uuid(user_id):
        logger.error(f"The id({user_id}) is not a valid uuid.")
        raise InputError(message="The user's id must be a uuid.")

    try:
        user = User.query.filter_by(id=user_id).first()
    except Exception as e:
        logger.critical(f"Failed to query user({user_id}), details: {e}")
        raise DatabaseError(message="There are errors when find in database.")

    if not user:
        logger.error(f"This user({user_id}) doesn't exist.")
        raise NotFoundError(message="This user doesn't exist.")

    if not user.is_activated:
        logger.error(f"This user({user_id}) has been deactivated already.")
        raise PermissionError(
            message="This user has been deactivated already."
            "You can not redeactivate him/her again."
        )

    # Deactivate user in database
    try:
        logger.debug(f"Before, user is activated : {user.is_activated}")
        user.is_activated = False
        db.session.merge(user)
        db.session.commit()
        logger.debug(f"After, user is activated : {user.is_activated}")
    except Exception as e:
        db.session.rollback()
        logger.critical(
            f"Failed to deactivate user({user_id}) in database, details: {e}"
        )
        raise DatabaseError(
            message="There are errors when deactivate user in database."
        )

    logger.info(f"The user({user_id}) has been deactivated successfully.")
    return {"message": "The user has been deactivated successfully."}
