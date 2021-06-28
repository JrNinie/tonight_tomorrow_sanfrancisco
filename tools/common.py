from uuid import UUID

def is_valid_uuid(uuid_to_test, version=4):
    """Check if uuid_to_test is a valid UUID

    Args:
        uuid_to_test (string): uuid to test
        version (int, optional): uuid's version (defaults to 4)

    Returns:
        boolean: if valid uuid return is True, else False
    """
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test