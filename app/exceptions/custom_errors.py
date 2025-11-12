# from fastapi import HTTPException, status
#
#
# class RepositoryException(HTTPException):
#     def __init__(self,
#                  status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
#                  detail: str = 'Repository error'
#     ):
#         HTTPException.__init__(self,
#                                status_code = status_code,
#                                detail = detail
#         )
#
#
# class NotFoundException(RepositoryException):
#     """Запись не найдена"""
#
#     def __init__(self, entity_name: str = "entity", ident: str = None, ident_val: str = None):
#         if ident and ident_val:
#             detail = f"{entity_name} with {ident}={ident_val} not found"
#         else:
#             detail = f"{entity_name} not found"
#
#         RepositoryException.__init__(
#             self,
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=detail
#         )
#
#
# class AlreadyExistsException(RepositoryException):
#     """Запись уже существует"""
#
#     def __init__(self, entity_name: str = "entity", ident: str = None, ident_val: str = None):
#         if ident and ident_val:
#             detail = f"{entity_name} with {ident}={ident_val} already exists"
#         else:
#             detail = f"{entity_name} already exists"
#
#         RepositoryException.__init__(
#             self,
#             status_code=status.HTTP_409_CONFLICT,
#             detail=detail
#         )
#
# class DatabaseException(RepositoryException):
#     """Ошибка базы данных"""
#     def __init__(self, detail: str = "Database error"):
#         RepositoryException.__init__(
#             self,
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=detail
#         )
# Не должно быть зависимости от HTTPException нужно независимую директорию exceptions для перехода из crud.exceptions в api.exceptions
