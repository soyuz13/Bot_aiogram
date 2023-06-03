from aiogram.filters import BaseFilter
from aiogram.types import Message
from models.users import Admins


class IsAdmin(BaseFilter):
    # def __init__(self, admin_ids: list[int]) -> None:
    #     print(0)
    #     self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        # print(1)
        self.admin_ids = Admins.get_list()
        return message.from_user.id in self.admin_ids
