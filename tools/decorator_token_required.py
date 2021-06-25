from flask import request, current_app
from functools import wraps
import jwt
from models.user import User
from exceptions.errors import CredentialError, NotFoundError
from log.my_logger import get_logger

logger = get_logger()


def token_required(f):
    """Create token required decorator

    This defines the decorator which checks required token for actions.
    The token must be included in header with the name 'x-access-token'
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            logger.error("Required token is missing.")
            raise CredentialError(message="Required token is missing.")

        # Get jwt payload WITH verification
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )
            current_user = User.query.filter_by(
                id=data["id"], is_activated=True
            ).first()
            if not current_user:
                logger.error(
                    f"User({data['id']}) doesn't exist\
                     or is not activated."
                )
                raise NotFoundError(
                    message="This user doesn't exist or is not activated.\
                            Please contact your administrator."
                )
        except jwt.ExpiredSignatureError:
            logger.error("This token is expired.")
            raise CredentialError(message="This token is expired.")
        except jwt.InvalidSignatureError:
            logger.error("This token is wrong.")
            raise CredentialError(message="This token is wrong.")

        logger.info("Received token is valid.")
        return f(current_user, *args, **kwargs)

    return decorated
