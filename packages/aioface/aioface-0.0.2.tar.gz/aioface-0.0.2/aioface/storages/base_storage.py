import typing


class BaseStorage:
    async def close(self) -> None:
        raise NotImplementedError

    @classmethod
    def check_user_id(cls, user_id: str) -> str:
        if user_id is None:
            raise ValueError('user_id parameter must be provided')
        return user_id

    async def get_data(self, user_id: str) -> typing.Dict:
        raise NotImplementedError

    async def set_data(self, user_id: str, data: typing.Dict):
        raise NotImplementedError

    async def update_data(self, user_id: str, data: typing.Dict):
        raise NotImplementedError

    async def reset_data(self, user_id: str):
        await self.update_data(user_id=user_id, data=dict())
