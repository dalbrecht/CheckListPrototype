from dataclasses import dataclass
from .storable import Storable
from CheckList.repositories import ChecklistRepository
from typing import Optional
from .user import User


@dataclass
class Checklist(Storable):
    repository: ChecklistRepository
    name: str = ""
    owner: Optional[User] = None
    done: bool = False

    def __post_init__(self):
        super().__init__(self.repository)
