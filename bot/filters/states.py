from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage



class FSMTodoFill(StatesGroup):
    fill_content = State()
    fill_name = State()
    fill_deadline = State()

class FSMTodoEdit(StatesGroup):
    edit = State()
    edit_content = State()
    edit_name = State()
    edit_date = State()
    delete_task = State()

class FSMSearch(StatesGroup):
    filter = State()
    filter_by_name = State()
    filter_by_content = State()
    filter_by_deadline = State()

class CustomRedisStorage(RedisStorage):
    async def set_data(self, key: StorageKey, data: dict) -> None:
        await super().set_data(key, data)

        data_key = f"fsm:{key.user_id}:{key.chat_id}:data"
        if self.state_ttl:
            await self.redis.expire(data_key, self.state_ttl)

    async def set_state(self, key: StorageKey, state: str) -> None:
        await super().set_state(key, state)
        state_key = f"fsm:{key.user_id}:{key.chat_id}:state"
        if self.state_ttl:
            await self.redis.expire(state_key, self.state_ttl)