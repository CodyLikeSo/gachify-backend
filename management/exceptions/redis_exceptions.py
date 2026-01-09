# redis_exceptions.py

from management.exceptions.exceptions import AppException
from fastapi import status


class CantConnectRedisHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t connect to redis: {e}"


class CantFetchDataFromRedisHttpException(AppException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Can`t get data from redis"


class RedisSetHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t set data in redis for email: {e}"


class RedisGetHttpException(AppException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Can`t get data from redis for email: {e}"
