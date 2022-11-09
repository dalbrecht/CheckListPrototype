from typing import Any

from .repository import Repository
from CheckList.objects.user import User
from sqlalchemy.engine import Engine


class UserRepository(Repository):
    @property
    def type(self) -> Any:
        return User

    @property
    def _table_name(self) -> Any:
        return "USERS"

    def __init__(self, engine: Engine):
        super().__init__(engine)
