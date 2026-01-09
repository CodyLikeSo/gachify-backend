# users_exceptions.py

from management.exceptions.exceptions import AppException
from fastapi import status


class EmailAlreadyUsedHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Email already used"


class UserActivityHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User with this email does not exist or already active"


class InvalidChallengeDataHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid challenge data"


class ChallengeExpiredDataHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Challenge expired"


class RegistrationHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Registration failed: {e}"


class AuthenticationHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Cant login: {e}"


class UserNotFoundOrAlreadyActiveHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User with this email does not exist or already active"


class RequestAlreadySendHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Request to activity already send"


class InvalidOrExpiredCodeHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid code or expired"


class InvalidCodeFormatException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid code"
