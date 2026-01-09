from typing import Generic, TypeVar, Literal
from pydantic import BaseModel

T = TypeVar("T")


class CreateResponse(BaseModel, Generic[T]):
    status: Literal[201] = 201
    detail: T
