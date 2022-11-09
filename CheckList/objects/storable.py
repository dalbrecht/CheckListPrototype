from dataclasses import dataclass
import uuid
from CheckList.repositories.repository import Repository_Type
from typing import Type, TypeVar


@dataclass
class Storable:
    repository: Type[Repository_Type]
    id: str = ""

    def __init__(self, repository):
        self._repository = repository
        if self.id == "":
            self.id = str(uuid.uuid4())

    def save(self):
        self._repository.store_object(self)


Storable_Type = TypeVar("Storable_Type", bound=Storable)
