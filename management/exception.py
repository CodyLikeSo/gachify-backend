from fastapi import HTTPException, status


class AppException(HTTPException):
    default_status_code: int = 500
    default_detail: str = "Unexpected Error"

    def __init__(self, detail: str = None, status_code: int = None, **kwargs):
        final_detail = detail or self.default_detail
        final_status_code = status_code or self.default_status_code

        if kwargs and final_detail:
            final_detail = final_detail.format(**kwargs)

        super().__init__(status_code=final_status_code, detail=final_detail)


class UnexpectedHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Unexpected Error: {e}"


class UserAlreadyExistHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User with this email already exists"


class CantCreateUserHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Can`t create user. Check data validity."


class RedisSetHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t set value to redis"


class RedisGetHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t get value from redis"


class VerificationReHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Invalid verification code"


class EmailSendHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to send email: {}"


class UserNotFoundHttpException(AppException):
    default_status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Incorrect username or password"


class UserNotVerifiedHttpException(AppException):
    default_status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Not verified"


class InvalidPasswordHttpException(AppException):
    default_status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Incorrect username or password"


class JWTEncodingHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to generate authentication token"


class EmailRequiredHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Email is required"


class EmailTaskCreationHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to create email task"


class ResetCodeNotFoundHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Reset code not found or expired"


class InvalidResetCodeHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid reset code"


class InvalidRedisDataHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Invalid data format in Redis: {e}"


class PasswordUpdateHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't update password: {e}"


class NoSerializerHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "No serializer configured for this operation"


class CantCreateObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't create object: {e}"


class CantDeleteObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't delete object"


class ObjectNotFoundHttpException(AppException):
    default_status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Object not found"


class CantRetrieveObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't retrieve object"


class CantListObjectsHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't list objects"


class CantReplaceObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't replace object"


class CantModifyObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't modify object"
