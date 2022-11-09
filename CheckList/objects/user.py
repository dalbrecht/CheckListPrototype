from dataclasses import dataclass
from .storable import Storable
from typing import Optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from CheckList.repositories import UserRepository


@dataclass
class User(Storable):
    repository: Optional["UserRepository"] = None
    email_address: str = ""
    password_hash: Optional[str] = None

    def __post_init__(self):
        super().__init__(self.repository)
