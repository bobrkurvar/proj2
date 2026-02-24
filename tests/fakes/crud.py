import logging
from copy import deepcopy
from typing import Any

from app.domain import TaskExecutors

log = logging.getLogger(__name__)


class Table:

    def __init__(
        self,
        name,
        columns: list[str],
        rows: list[dict] | None = None,
        defaults: dict[str, Any] | None = None,
    ):
        self.name = name
        self.columns = columns
        self.rows = rows if rows else []
        self.defaults = defaults

    def __add__(self, other):
        # создаём новую таблицу
        new_table = Table(
            name=self.name,
            columns=self.columns.copy(),
            rows=deepcopy(self.rows),
            defaults=self.defaults,
        )

        if other.name is TaskExecutors:
            new_table.columns += ["executors"]

            for i in range(len(new_table.rows)):
                to_row = {}
                for row in other.rows or []:
                    if row["task_id"] == new_table.rows[i]["id"]:
                        to_row.update(
                            {"box_area": row["area"], "box_weight": row["weight"]}
                        )
                new_table.rows[i].update(to_row)
        return new_table


class FakeCrudError(Exception):

    def __init__(self, err: str):
        super().__init__()
        self.err = err

    def __str__(self):
        return self.err


class FakeStorage:

    def __init__(self):
        self.tables: dict[Any, Table] = {}
        self.to_join = {
            "size": TaskExecutors,
        }

    def register_tables(self, models: list[Table]):
        for model in models:
            self.tables[model.name] = model

    def add(self, model, **columns):
        table = self.tables[model]
        if table.rows is None:
            table.rows = []
        for table_column in table.columns:
            if table_column not in columns:
                columns.update(
                    {
                        table_column: (
                            table.defaults[table_column] if table.defaults else None
                        )
                    }
                )
                if isinstance(table.defaults[table_column], int):
                    table.defaults[table_column] += 1

        table.rows.append(columns)
        return columns

    def read(
        self, model, to_join=None, distinct=None, limit=None, offset=None, **filters
    ):
        table = self.tables[model]
        if not table.rows:
            return []

        result = []
        if to_join:
            for t in to_join:
                # log.debug("FAKE JOIN %s", t)
                t = self.to_join.get(t, t)
                t = self.tables[t]
                table = table + t

        for row in table.rows:
            if all(row.get(k) == v for k, v in filters.items()):
                result.append(row)

        if distinct:
            if isinstance(distinct, str):
                distinct = [distinct]
            seen = set()
            unique_result = []
            for row in result:
                key = tuple(row.get(f) for f in distinct)
                # log.debug("DISTINCT: %s", key)
                if key not in seen:
                    seen.add(key)
                    unique_result.append(row)
            result = unique_result

        if offset:
            result = result[offset:]
        if limit:
            result = result[:limit]

        return result

    def update(self, model, filters, **values):
        table = self.tables[model]
        # log.debug("UPDATE TABLE %s FILTERS: %s, VALUES: %s", model, filters, values)
        for i in range(len(table.rows)):
            if all(table.rows[i][f] == v for f, v in filters.items()):
                for k, v in values.items():
                    table.rows[i][k] = v

    def delete(self, model, **filters):
        table = self.tables[model]
        del_res = []
        # log.debug("DELETE TABLE %s FILTERS: %s", model, filters)
        for i in range(len(table.rows)):
            if all(table.rows[i][f] == v for f, v in filters.items()):
                del_res.append(table.rows[i])
                del table.rows[i]
        if not del_res:
            raise FakeCrudError(f"NOT EXISTS filters: {filters}")
        return del_res


class FakeCRUD:
    _session_factory = None

    def __init__(self, storage: FakeStorage):
        self.storage = storage

    async def create(self, model, session=None, **columns):
        return self.storage.add(model, **columns)

    async def read(
        self,
        model,
        session=None,
        to_join=None,
        distinct=None,
        limit=None,
        offset=None,
        **filters,
    ):
        return self.storage.read(
            model,
            to_join=to_join,
            distinct=distinct,
            limit=limit,
            offset=offset,
            **filters,
        )

    async def update(self, model, filters: dict, session=None, **values):
        return self.storage.update(model, filters, **values)

    async def delete(self, model, session=None, **filters):
        return self.storage.delete(model, **filters)


class FakeUoW:
    def __init__(self, *args, **kwargs):
        self.committed = False
        self.session = self  # если session нужен, но не используется

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def commit(self):
        self.committed = True
