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
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Error: {e}"


class CantConnectPostgresHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t connect to postgres: {e}"


class CantCheckMigrationsHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t check migrations: {e}"


class CantConnectRedisHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t connect to redis: {e}"


class EmailAlreadyUsedHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Email already used"


class PhoneAlreadyUsedHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Phone already used"


class UserActivityHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User with this email does not exist or already active"


class CantFetchDataFromRedisHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Can`t get data from redis"


class InvalidChallengeDataHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid challenge data"


class ChallengeExpiredDataHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Challenge expired"


class RegistrationHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Registration failed: {e}"


class RedisSetHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t set data in redis for email: {e}"


class RedisGetHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t get data from redis for email: {e}"


class EmailSendHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t send email: {e}"


class RequestAlreadySendHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Request to activity already send"


class InvalidOrExpiredCodeHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid code or expired"


class InvalidCodeFormatException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid code"


class UserNotFoundOrAlreadyActiveHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User with this email does not exist or already active"


class NoSerializerHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "No serializer configured for this operation"


class CantCreateObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't create object: {e}"


class CantDeleteObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't delete object: {e}"


class ObjectNotFoundHttpException(AppException):
    default_status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Object not found"


class CantRetrieveObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't retrieve object"


class CantListObjectsHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't list objects: {e}"


class CantReplaceObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't replace object"


class CantModifyObjectHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can't modify object"


class AuthenticationHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Cant login: {e}"
