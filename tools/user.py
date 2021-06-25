from uuid import UUID
from exceptions.errors import InputError
from log.my_logger import get_logger

logger = get_logger()


def verify_data_form(data):
    """Verify the nullable & form of data

    Args:
        data (object/None): data in the body of a request

    Raises:
        InputError:  no data OR not send in Json OR not a dict
    """

    if not data:
        logger.error("No related data or form not in json.")
        raise InputError(
            message="No data in your request(body) or it's form not in json."
        )

    if not isinstance(data, dict):
        logger.error("The data of the request must be a dict/json.")
        raise InputError(message="The data of the request must be a dict.")


def is_uuid(id, version=4):
    """uuid check

    Args:
        id (string): id to be checked
        version (int, optional): uuid version. Defaults to 4.

    Raises:
        InputError: id must be a string at first

    Returns:
        boolean: if it's a valid uuid
    """
    try:
        """
        If id is a valid hex code but not a valid uuid,
        UUID() will convert it to a valid uuid anyway.
        In order to avoid this, we check original version (without hypen)
        with the hex code, if they as the same, this id is a valid uuid.
        """
        id = id.lower()
        uid = UUID(id, version=version)
        return uid.hex == id.replace("-", "")
    except AttributeError:
        logger.error(f"User id(uuid) must be a string, not {type(id)}.")
        raise InputError(
            message=f"User id(uuid) must be a string, not {type(id)}."
        )
    except ValueError:
        logger.error(f"The id({id}) is not a valid uuid.")
        return False


def verify_type_integrity_of_data(template, data):
    """Check integrity & type

    It allows to check if data includs all columns required by template,
    and ensure they have also the type defined by template.

    Args:
        template (dict): key is the column name and value is it's type
            example
                    template = {
                    "first_name": str,
                    "password": str,
                    "is_activated": bool,
                    "is_admin": bool,
                    "last_name": str,
                    "mail": str,
                    "liked_movie_id": list,
                    }
        data (dict): data in the body of a request

    Raises:
        InputError: Error info about input
    """
    # All required columns check
    for key_required in template.keys():
        if key_required not in [key for key in data.keys()]:
            logger.error(f"'{key_required}' is missing.")
            raise InputError(f"You don't provide '{key_required}'(required).")

    # Data type check
    for key_required, type_required in template.items():
        if not isinstance(data[key_required], type_required):
            logger.error(
                f"{key_required}'s type must be a {type_required},\
                    not a {type(data[key_required])}."
            )
            raise InputError(
                message=f"{key_required}'s type must be a {type_required},\
                    not {type(data[key_required])}."
            )
