import typing

from aioface.storages.base_storage import BaseStorage
from aioface.storages.fsm.types import State


class FSM:
    def __init__(self, storage: BaseStorage, user_id: str):
        self.storage = storage
        self.user_id = self.storage.check_user_id(user_id=user_id)

    async def get_state(self) -> typing.Dict:
        return await self.storage.get_data(user_id=self.user_id)['state']

    async def set_state(self, state: State):
        await self.storage.set_data(user_id=self.user_id,
                                    data={'state': state})

    async def reset_state(self):
        await self.storage.set_data(user_id=self.user_id,
                                    data={'state': None})
