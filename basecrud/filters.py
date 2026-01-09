from fastapi import Query
from pydantic import BaseModel


class BaseFilter(BaseModel):
    pass

    class Meta:
        filter_values: set

        model = None


class Filter(BaseFilter):
    def filter(self, query: Query):
        for field_name in self.Meta.filter_values:
            field_value = getattr(self, field_name)
            if field_value is not None:
                field = getattr(self.Meta.model, field_name)
                query = query.filter(
                    field.ilike(f"%{field_value}%")
                    if isinstance(field_value, str)
                    else field == field_value
                )
        return query

    def sort(self, query: Query):
        if self.order_by:
            if "," in self.order_by:
                order_fields = set()
                for field_name in self.order_by.split(","):
                    order_field = getattr(self.Meta.model, field_name.lstrip("-"))
                    order_fields.add(
                        order_field.desc()
                        if field_name.startswith("-")
                        else order_field.asc()
                    )
                query = query.order_by(*order_fields)
            else:
                direction = self.order_by.startswith("-")
                clean_field_name = self.order_by.lstrip("-")
                order_field = getattr(self.Meta.model, clean_field_name)
                query = query.order_by(
                    order_field.desc() if direction else order_field.asc()
                )
        return query

    def apply(self, query: Query):
        query = self.filter(query)
        query = self.sort(query)
        return query
