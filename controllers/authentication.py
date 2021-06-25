from werkzeug.security import check_password_hash
import jwt
import datetime
from models.user import User
from exceptions.errors import CredentialError, DatabaseError
from log.my_logger import get_logger

logger = get_logger()


def verify_login(auth, secret_key):

    if not auth or not auth.username or not auth.password:
        logger.error("Missing username or password.")
        raise CredentialError(
            message="Your email account and/or password is/are missing."
        )

    # the username in auth matches MAIL of table t_user
    # (column username doesn't exist in table t_user)
    username = auth.username.lower()
    logger.debug(f"Username is {username}")
    try:
        user = User.query.filter_by(mail=username, is_activated=True).first()
    except Exception as e:
        logger.error(f"Failed to find user '{username}' in db, details: {e}")
        raise DatabaseError(message="There are errors when find user in db.")

    if not user:
        logger.error(f"User {username} doesn't exist or is deactivated")
        raise CredentialError(message="User doesn't exist or is deactivated.")

    if check_password_hash(user.password, auth.password):
        # Generate token
        utc_time = datetime.datetime.utcnow()
        timedelta = datetime.timedelta(minutes=30)
        token = jwt.encode(
            {
                "id": str(user.id),
                "exp": utc_time + timedelta,
            },
            secret_key,
            algorithm="HS256",
        )
        logger.info("Token has been generated successfully.")
        return {"token": token}
    else:
        logger.error(f"User ({username}) tried to login but wrong password")
        raise CredentialError(message="Your password is incorrect.")
