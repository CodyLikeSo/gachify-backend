from basecrud.crud import BaseViewSet
from users.filters import UsersFilter
from users.models import Users
from users.schemas import UsersList, UsersCreate, UsersReplace, UsersModify
from uuid import UUID

serializers = {
    "get": UsersList,
    "post": UsersCreate,
    "put": UsersReplace,
    "patch": UsersModify,
}

UsersCrud = BaseViewSet(
    model=Users,
    serializers=serializers,
    filter_class=UsersFilter,
    pk_settings=(UUID, "uuid"),
)
