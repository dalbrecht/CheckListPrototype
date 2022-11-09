from .repository import Repository
from sqlalchemy.engine import Engine


class ChecklistRepository(Repository):
    def __init__(self, engine: Engine):
        super().__init__(engine=engine)
