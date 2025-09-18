from fastapi import APIRouter, status, HTTPException, Depends
from db.models import Todo
from db import get_db_manager, Crud
from app.api.schemas.todo import TodoInput, TodoOutput, TodoUpdate
from app.exceptions.schemas import ErrorResponse
from sqlalchemy.exc import IntegrityError
from datetime import date
from typing import List, Annotated
import logging

router = APIRouter(tags=['Todo'])
log = logging.getLogger(__name__)
dbManagerDep = Annotated[Crud, Depends(get_db_manager)]

@router.get('',
            status_code=status.HTTP_200_OK,
            response_model=List[TodoOutput],
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'detail': 'Задачи не найдены',
                    'model': ErrorResponse
                }
            },
            summary='Получение задач'
)
async def read_todo_list(ident: str,
                         manager: dbManagerDep,
                         ident_val: int,
                         limit: int | None = None,
                         offset: int | None = None,
                         order_by: str | None = None
):
    log.debug('запрос на чтение задач по %s со значением: %s limit: %s, offset: %s', ident, ident_val, limit, offset)
    res = await manager.read(Todo, ident=ident, ident_val=ident_val, limit=limit, offset=offset, order_by = order_by)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задачи не найдены'
        )
    return res

@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=TodoOutput,
             responses={
                status.HTTP_409_CONFLICT: {
                    'detail': 'Задача с таки id уже существует',
                    'model': ErrorResponse
                }
             },
             summary='создание задачи'
)
async def create_task(todo: TodoInput, manager: dbManagerDep):
    todo = todo.model_dump()
    todo.update(deadline=date(**todo.get('deadline')))
    log.debug('запрос на создание задания')
    try:
        todo = await manager.create(Todo, **todo)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Задача с таким id уже существует'
        )
    return todo

@router.patch('',
              summary='обновление задачи',
              responses={
                  status.HTTP_409_CONFLICT: {
                      'detail': 'Задача для обновления не найдена',
                      'model': ErrorResponse
                  },
                  status.HTTP_204_NO_CONTENT: {
                      'detail': 'Пустое тело ответа'
                  }
              },
              status_code=status.HTTP_204_NO_CONTENT
)
async def update_task(todo: TodoUpdate, manager: dbManagerDep):
    todo_data = todo.model_dump()
    for_update = []
    del todo_data['is_delete']
    if not todo_data['name']:
        del todo_data['name']
    else:
        for_update.append('name')

    if not todo_data['content']:
        del todo_data['content']
    else:
        for_update.append('content')

    if not todo_data['deadline']:
        del todo_data['deadline']
    else:
        todo_data.update(deadline=date(day=todo_data['deadline']['day'], month=todo_data['deadline']['month'], year=todo_data['deadline']['year']))
        for_update.append('deadline')
    log.debug('запрос на обновление в задании '
             '%s параметров: %s', todo.ident_val, *for_update)
    todo = await manager.update(Todo, **todo_data)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача для обновления не найдена'
        )
    log.info('в задаче: %s обновлены параметры: %s', todo.ident_val, *for_update)

@router.delete('/{todo_id}',
               summary='Удаление задачи по id или всех задач',
               status_code=status.HTTP_200_OK,
               response_model=TodoOutput,
               responses={
                   status.HTTP_404_NOT_FOUND: {
                       'detail' : 'Задача для удаления не найдена',
                       'model': ErrorResponse
                   }
               }
)
async def delete_task_by_id_or_all(todo_id: int | None, manager: dbManagerDep):
    if todo_id is None:
        await manager.delete(model=Todo)
    else:
        todo = await manager.delete(model=Todo, ident_val=todo_id)
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Задача для удаления не найдена'
            )
        return todo
