from dataclasses import dataclass
from .storable import Storable
from CheckList.repositories import TaskRepository
from CheckList.objects.checklist import Checklist
from typing import Optional


@dataclass
class Task(Storable):
    repository: Optional[TaskRepository] = None
    label: Optional[str] = None
    done: bool = False
    checklist: Optional[Checklist] = None

    def __post_init__(self):
        super().__init__(self.repository)
