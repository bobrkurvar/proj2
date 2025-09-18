class RepositoryError(Exception):
    """Базовое исключение репозитория"""
    pass

class NotFoundError(RepositoryError):
    """Не найдена запись в базе"""

    def __init__(self, entity_name: str, ident: str | None = None, ident_val = None):
        self.entity_name = entity_name
        self.ident = ident
        self.ident_val = ident_val
        if ident and ident_val:
            super().__init__(f"{entity_name} with {ident}={ident_val} not found")
        else:
            super().__init__(f"{entity_name} not found")


class AlreadyExistsError(RepositoryError):
    """Запись с таким атрибутом уже существует в базе"""

    def __init__(self, entity: str, attr: str | None = None, attr_val = None):
        self.attr = attr
        self.ident_val = attr_val
        self.entity = entity
        if attr and attr_val:
            super().__init__(f"Запись с {attr} = {attr_val} в таблице {entity} уже существует")
        else:
            super().__init__(f"Запись с таким id в таблице {entity} уже существует")


class DatabaseError(RepositoryError):
    pass
