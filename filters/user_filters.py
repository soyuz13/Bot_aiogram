from aiogram.filters import BaseFilter
from aiogram.types import Message
from models.users import Users


class IsUser(BaseFilter):
    # def __init__(self, admin_ids: list[int]) -> None:
    #     self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        self.user_ids = Users.get_list()
        return message.from_user.id in self.user_ids

