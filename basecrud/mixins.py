from database.db import get_db
from typing import List, Optional
from basecrud.filters import Filter
from pydantic import BaseModel
from fastapi import Query

from management.exceptions.exceptions import (
    NoSerializerHttpException,
    CantCreateObjectHttpException,
    ObjectNotFoundHttpException,
    CantDeleteObjectHttpException,
    CantRetrieveObjectHttpException,
    CantListObjectsHttpException,
    CantReplaceObjectHttpException,
    CantModifyObjectHttpException,
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.responses import Response


class CreateMixin:
    def _register_post_route(self):
        create_serializer = self.serializers.get("post")
        if not create_serializer:
            raise NoSerializerHttpException()

        @self.router.post("/")
        async def create_endpoint(
            item: create_serializer, db: AsyncSession = Depends(get_db)
        ):
            return await self.create(item, db)

    async def create(self, item: BaseModel, db: AsyncSession):
        try:
            db_item = self.model(**item.model_dump())
            db.add(db_item)
            await db.commit()
            await db.refresh(db_item)
            return db_item
        except Exception as e:
            await db.rollback()
            raise CantCreateObjectHttpException(e=str(e))


class DeleteMixin:
    def _register_delete_route(self):
        pk_type, pk_name = self.pk_settings

        @self.router.delete("/{item_id}/")
        async def delete_endpoint(
            item_id: pk_type,
            db: AsyncSession = Depends(get_db),
        ):
            return await self.delete(item_id, db)

    async def delete(self, item_id, db: AsyncSession):
        pk_type, pk_name = self.pk_settings
        pk_column = getattr(self.model, pk_name)

        try:
            result = await db.execute(select(self.model).where(pk_column == item_id))
            db_item = result.scalar_one_or_none()

            if not db_item:
                raise ObjectNotFoundHttpException()

            await db.delete(db_item)
            await db.commit()
            return Response(status_code=204)
        except ObjectNotFoundHttpException:
            raise
        except Exception as e:
            await db.rollback()
            raise CantDeleteObjectHttpException(e=str(e))


class RetrieveMixin:
    def _register_retrieve_route(self):
        pk_type, pk_name = self.pk_settings

        @self.router.get("/{item_id}/")
        async def retrieve_endpoint(
            item_id: pk_type,
            db: AsyncSession = Depends(get_db),
        ):
            return await self.retrieve(item_id, db)

    async def retrieve(self, item_id, db: AsyncSession):
        _, pk_name = self.pk_settings
        pk_column = getattr(self.model, pk_name)

        try:
            result = await db.execute(select(self.model).where(pk_column == item_id))
            db_item = result.scalar_one_or_none()

            if not db_item:
                raise ObjectNotFoundHttpException()

            return db_item
        except ObjectNotFoundHttpException:
            raise
        except Exception:
            raise CantRetrieveObjectHttpException()


class ListMixin:
    def _register_list_route(self):
        list_serializer = self.serializers.get("get")
        if not list_serializer:
            raise NoSerializerHttpException()

        if self.filter_class:

            @self.router.get("/", response_model=List[list_serializer])
            async def list_endpoint_with_filter(
                filter: Filter = Depends(self.filter_class),
                skip: int = Query(0, ge=0, description="Number of items to skip"),
                limit: int = Query(
                    100, ge=1, le=1000, description="Number of items to return"
                ),
                db: AsyncSession = Depends(get_db),
            ):
                return await self.get_list(db, filter, skip=skip, limit=limit)

        else:

            @self.router.get("/", response_model=List[list_serializer])
            async def list_endpoint_without_filter(
                skip: int = Query(
                    default=0, ge=0, description="Number of items to skip"
                ),
                limit: int = Query(
                    default=100, ge=1, le=1000, description="Number of items to return"
                ),
                db: AsyncSession = Depends(get_db),
            ):
                return await self.get_list(db, None, skip=skip, limit=limit)

    async def get_list(
        self,
        db: AsyncSession,
        filter_params: Optional[Filter] = None,
        skip: int = 0,
        limit: int = 100,
    ):
        try:
            stmt = select(self.model)

            if filter_params:
                stmt = filter_params.apply(stmt)

            stmt = stmt.offset(skip).limit(limit)

            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception:
            raise CantListObjectsHttpException()


class ReplaceMixin:
    def _register_replace_route(self):
        pk_type, pk_name = self.pk_settings
        put_serializer = self.serializers.get("put")
        if not put_serializer:
            raise NoSerializerHttpException()

        @self.router.put("/{item_id}/")
        async def replace_endpoint(
            item_id: pk_type,
            update_data: put_serializer,
            db: AsyncSession = Depends(get_db),
        ):
            return await self.replace(item_id, update_data, db)

    async def replace(self, item_id, update_data: BaseModel, db: AsyncSession):
        _, pk_name = self.pk_settings
        pk_column = getattr(self.model, pk_name)

        try:
            result = await db.execute(select(self.model).where(pk_column == item_id))
            db_item = result.scalar_one_or_none()

            if not db_item:
                raise ObjectNotFoundHttpException()

            update_dict = update_data.model_dump()
            for field, value in update_dict.items():
                setattr(db_item, field, value)

            db.add(db_item)
            await db.commit()
            await db.refresh(db_item)
            return db_item
        except ObjectNotFoundHttpException:
            raise
        except Exception:
            await db.rollback()
            raise CantReplaceObjectHttpException()


class ModifyMixin:
    def _register_modify_route(self):
        pk_type, pk_name = self.pk_settings
        patch_serializer = self.serializers.get("patch")
        if not patch_serializer:
            raise NoSerializerHttpException()

        @self.router.patch("/{item_id}/")
        async def modify_endpoint(
            item_id: pk_type,
            update_data: patch_serializer,
            db: AsyncSession = Depends(get_db),
        ):
            return await self.modify(item_id, update_data, db)

    async def modify(self, item_id, update_data: BaseModel, db: AsyncSession):
        _, pk_name = self.pk_settings
        pk_column = getattr(self.model, pk_name)

        try:
            result = await db.execute(select(self.model).where(pk_column == item_id))
            db_item = result.scalar_one_or_none()

            if not db_item:
                raise ObjectNotFoundHttpException()

            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(db_item, field, value)

            db.add(db_item)
            await db.commit()
            await db.refresh(db_item)
            return db_item
        except ObjectNotFoundHttpException:
            raise
        except Exception:
            await db.rollback()
            raise CantModifyObjectHttpException()
