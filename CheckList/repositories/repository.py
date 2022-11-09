import typing
from types import NoneType

from sqlalchemy.engine import Engine
from abc import ABCMeta, abstractmethod
import dataclasses
from typing import TypeVar, Dict, Union, Any, Tuple, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from CheckList.objects.storable import Storable_Type


def _max_type(types: Tuple[Any]):
    max_type = None
    for t in types:
        try:
            if t.is_instance(type(None)):
                continue
        except AttributeError:
            pass
        if t in [bool, int] and max_type is None:
            max_type = int
        elif t == float and max_type in [int] or max_type is None:
            max_type = float
        elif t not in [float, int] and not isinstance(t, NoneType):
            max_type = str
    return max_type


class Repository:
    __metaclass__ = ABCMeta

    def __init__(self, engine: Engine):
        self._engine = engine
        self._types: Optional[Dict[str, str]] = None

    @property
    @abstractmethod
    def type(self) -> Any:
        pass

    @property
    @abstractmethod
    def _table_name(self) -> Any:
        pass

    def ensure_table_exists(self):
        self._engine.execute(self.create_sql)

    @property
    def create_sql(self) -> str:
        type_clauses = [f"{k} {v}" for (k, v) in self.sql_types.items() if k != "id"]
        clauses_str = ", ".join(type_clauses)
        create_string = """
CREATE TABLE IF NOT EXISTS {table_name} (
  id VARCHAR PRIMARY KEY,
  {clauses_str})
""".format(
            table_name=self._table_name, clauses_str=clauses_str
        )
        return create_string

    @property
    def fields(self):
        return {
            field.name: field.type
            for field in dataclasses.fields(self.type)
            if field.name != "repository"
        }

    @property
    def sql_types(self):
        if self._types is not None:
            return self._types
        out_dict: Dict[str, str] = dict()
        for k, v in self.fields.items():
            if typing.get_origin(v) is Union:
                t = _max_type(typing.get_args(v))
            else:
                t = v
            if t in [bool, int]:
                out_dict[k] = "INTEGER"
            elif t in [float]:
                out_dict[k] = "FLOAT"
            elif t in [str]:
                out_dict[k] = "VARCHAR"

        self._types = out_dict
        return self._types

    def validate_type(self, object: Any) -> bool:
        return self.type == type(object)

    def store_object(self, storable_object: "Storable_Type"):
        assert self.validate_type(storable_object)
        upsert = """
INSERT INTO {table_name}({fields})
  VALUES({values})
  ON CONFLICT(ID) DO UPDATE SET
    {update_vals}
    """
        type_fields = self.fields
        values: List[Any] = list()
        update_vals: List[str] = list()
        values_clause = list()
        lookup = dict(
            (field.name, getattr(storable_object, field.name))
            for field in dataclasses.fields(storable_object)
        )
        for field in type_fields.keys():
            values.append(lookup[field])
            values_clause.append("?")
            update_vals.append(f"{field}=?")

        values_clause_str = ", ".join(values_clause)
        update_vals_str = ", ".join(update_vals)
        binding_values = values + values
        fields_str = ", ".join(type_fields.keys())
        query = upsert.format(
            table_name=self._table_name,
            fields = fields_str,
            values=values_clause_str,
            update_vals=update_vals_str,
        )
        self._engine.execute(query, binding_values)

    def fetch(self, object_id: str):
        q = f"SELECT * FROM {self._table_name} WHERE id = ?"
        out = list()
        with self._engine.begin() as connection:
            result = connection.execute(q, [object_id])
            for record in result:
                transform = {k.lower(): v for (k, v) in record.items()}
                out.append(self.type(**transform))
        assert len(out) < 2
        if len(out) == 1:
            return out[0]
        return None

    def fetch_all(self):
        q = f"SELECT * FROM {self._table_name}"
        out = list()
        with self._engine.begin() as connection:
            result = connection.execute(q)
            for record in result:
                out.append(self.type(**record))


Repository_Type = TypeVar("Repository_Type", bound=Repository)
