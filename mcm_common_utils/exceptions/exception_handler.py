"""
generic exception handler

all the thrown api error exceptions will be handled here
and return valid error response to the client
"""
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def extract_error_code(data):
    try:
        if data.get('detail', {}).get('code') is not None:
            return data['detail']['code']
        return None
    except Exception as ex:
        logger.debug(f"unexpected error response data object received: {str(ex)}")
        return None


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)  # Use the default exception handler to get the standard response

    if response is not None:
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            response.data = {
                "status_code": response.status_code,
                "error_code": extract_error_code(response.data),
                "error_message": response.data.get('detail', 'Internal Server Error'),
            }
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {
                "status_code": response.status_code,
                "error_code": extract_error_code(response.data),
                "error_message": response.data.get('detail', 'Bad Request'),
            }
        return response
    response_data = {
        "status_code": 500,
        "error_code": None,
        "error_message": 'Internal Server Error',
    }
    return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
