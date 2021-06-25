from .APIException import APIException


class CredentialError(APIException):
    def __init__(
        self,
        message="There is a credential error.",
        error_code="CREDENTIAL_ERROR",
        status_code=401,
        headers=None,
    ):
        APIException.__init__(self, message, error_code, status_code, headers)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.headers = headers


class PermissionError(APIException):
    def __init__(
        self,
        message="You are not authorized to perform this operation.",
        error_code="PERMISSION_ERROR",
        status_code=403,
        headers=None,
    ):
        APIException.__init__(self, message, error_code, status_code, headers)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.headers = headers


class InputError(APIException):
    def __init__(
        self,
        message="There is at least one mistake in your input.",
        error_code="INPUT_ERROR",
        status_code=422,
        headers=None,
    ):
        APIException.__init__(self, message, error_code, status_code, headers)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.headers = headers


class NotFoundError(APIException):
    def __init__(
        self,
        message="We don't find what your're looking for.",
        error_code="NOT_FOUND_ERROR",
        status_code=400,
        headers=None,
    ):
        APIException.__init__(self, message, error_code, status_code, headers)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.headers = headers


class DatabaseError(APIException):
    def __init__(
        self,
        message="mistakes in database",
        error_code="DATABASE_ERROR",
        status_code=500,
        headers=None,
    ):
        APIException.__init__(self, message, error_code, status_code, headers)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.headers = headers
