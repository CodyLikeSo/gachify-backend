from fastapi import APIRouter
from database.db import Base
from pydantic import BaseModel
from basecrud.filters import Filter
from basecrud.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    RetrieveMixin,
    ReplaceMixin,
    ModifyMixin,
)
from typing import Type, Dict, Tuple


class BaseViewSet(
    CreateMixin,
    DeleteMixin,
    ListMixin,
    RetrieveMixin,
    ReplaceMixin,
    ModifyMixin,
):
    def __init__(
        self,
        model: Type[Base],
        serializers: Dict[str, Type[BaseModel]],
        filter_class: Type[Filter] = None,
        pk_settings: Tuple[type, str] = (str, "id"),
    ):
        self.model = model
        self.serializers = serializers
        self.filter_class = filter_class

        self.table_name = model.__tablename__
        self.router = APIRouter(prefix=f"/{self.table_name}", tags=[self.table_name])

        self.pk_settings = pk_settings

        if serializers is not None:
            if serializers.get("post"):
                self._register_post_route()
            if serializers.get("get"):
                self._register_list_route()
            if serializers.get("patch"):
                self._register_modify_route()
            if serializers.get("put"):
                self._register_replace_route()
            self._register_delete_route()
            self._register_retrieve_route()
