from flask import make_response
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    """Implement user-defined exception

    This exception take a proper readable message, error code,
    status code and headers.
    And it ensures the Content-Type is application/json.
    It could be inherited by other user-defined errors/exceptions of this api.

    Args:
        HTTPException : HTTPException from werkzeug.exceptions
    """

    def __init__(
        self,
        message="There is a mistake",
        error_code="SERVER_ERROR",
        status_code=500,
        headers=None,
    ):
        HTTPException.__init__(self, message, None)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.headers = headers

    def get_body(self, environ=None):
        body = dict(
            message=self.message,
            error_code=self.error_code,
        )
        return body

    def get_headers(self, environ=None):
        return [("Content-Type", "application/json")]

    def get_response(self, environ=None):
        headers = self.get_headers(environ)
        return make_response(self.get_body(environ), self.status_code, headers)
