from typing import Optional
from users.models import Users
from basecrud.filters import Filter


class UsersFilter(Filter):
    name: Optional[str] = None
    telegram: Optional[str] = None

    order_by: Optional[str] = None

    class Meta:
        filter_values = {"name"}
        model = Users
