"""
generic exception classes can be used to return a error response
"""
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    status_code = 400
    default_detail = "Bad Request"
    default_code = "4000"

    def __init__(self, error_code=default_code, error_message=default_detail):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(self.error_message)


class InvalidRequestException(APIException):
    status_code = 400
    default_detail = "Bad Request"
    default_code = "4000"

    def __init__(self, error_code=default_code, error_message=default_detail):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(self.error_message)


class RequestSerializationException(APIException):
    status_code = 400
    default_detail = "Bad Request"
    default_code = "4000"

    def __init__(self, error_code=default_code, error_message=default_detail):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(self.error_message)


class ResponseSerializationException(APIException):
    status_code = 500
    default_code = "5000"
    default_detail = 'Internal Server Error'

    def __init__(self, error_code=default_code, error_message=default_detail):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(self.error_message)


class InternalServiceConnectException(APIException):
    status_code = 500
    default_code = "5000"
    default_detail = 'Internal Server Error'

    def __init__(self, error_code=default_code, error_message=default_detail):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(self.error_message)
