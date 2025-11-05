from fastapi import APIRouter, status, Depends
from db.models import Todo
from db import get_db_manager, Crud
from app.api.schemas.todo import TodoInput, TodoOutput, TodoUpdate
from app.exceptions.schemas import ErrorResponse
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
            summary='Получение задач по id пользователя'
)
async def read_todo_by_criteria(
                         manager: dbManagerDep,
                         doer_id: int,
                         limit: int | None = None,
                         offset: int | None = None,
                         order_by: str | None = None
):
    log.debug('запрос на чтение задач по doer_id со значением: %s limit: %s, offset: %s', doer_id, limit, offset)
    res = await manager.read(Todo, ident="doer_id", ident_val=doer_id, limit=limit, offset=offset, order_by = order_by)
    return res

@router.get('/{todo_id}',
            status_code=status.HTTP_200_OK,
            response_model=TodoOutput,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'detail': 'Задача с таким id не найдена',
                    'model': ErrorResponse
                }
            },
            summary='Получение задач по id'
)
async def read_todo_by_id(todo_id: int, manager: dbManagerDep):
    log.debug('ЗАПРОС НА ЧТЕНИЕ ЗАДАЧИ ПО ID %s', todo_id)
    res = await manager.read(Todo, ident_val=todo_id)
    return res

@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=TodoOutput,
             responses={
                status.HTTP_409_CONFLICT: {
                    'detail': 'Задача с таким id уже существует',
                    'model': ErrorResponse
                }
             },
             summary='Создание задачи'
)
async def create_task(todo: TodoInput, manager: dbManagerDep):
    todo = todo.model_dump()
    deadline = date(**todo.pop("deadline"))
    log.debug('запрос на создание задания')
    todo = await manager.create(Todo, **todo, deadline=deadline)
    log.debug(f"задача {todo} создана")
    return todo

@router.patch('',
              summary='обновление задачи',
              responses={
                  status.HTTP_404_NOT_FOUND: {
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
    log.debug('Запрос на обновление в задании '
             '%s параметров: %s', todo.ident_val, *for_update)
    await manager.update(Todo, **todo_data)

@router.delete('/{todo_id}',
               summary='Удаление задачи по id',
               status_code=status.HTTP_200_OK,
               response_model=TodoOutput,
               responses={
                   status.HTTP_404_NOT_FOUND: {
                       'detail' : 'Задача для удаления не найдена',
                       'model': ErrorResponse
                   }
               }
)
async def delete_task_by_id(todo_id: int, manager: dbManagerDep):
    todo = await manager.delete(model=Todo, ident_val=todo_id)
    return todo

# @router.delete('',
#                summary='Удаление по критериям или всех задач',
#                responses={
#                    status.HTTP_404_NOT_FOUND: {
#                        'detail': 'Задачи для удаление не найдены или список пуст',
#                        'model': ErrorResponse
#                    }
#                },
#                status_code=status.HTTP_204_NO_CONTENT
# )
# async def delete_task_by_criteria()

