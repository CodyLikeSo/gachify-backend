# postgres_exceptions.py

from management.exceptions.exceptions import AppException
from fastapi import status


class CantConnectPostgresHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t connect to postgres: {e}"


class CantCheckMigrationsHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t check migrations: {e}"


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
