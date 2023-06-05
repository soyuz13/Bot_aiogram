import json
from config import USER_LIST, ADMIN_LIST


class Users:
    filename = USER_LIST

    @classmethod
    def add(cls, id):
        with open(f'files/{cls.filename}', 'r') as fil:
            lst = json.load(fil)
        lst.append(id)
        with open(f'files/{cls.filename}', 'w') as fil:
            json.dump(lst, fil)
        return id

    @classmethod
    def remove(cls, id):
        with open(f'files/{cls.filename}', 'r') as fil:
            lst = json.load(fil)
        lst.remove(id)
        with open(f'files/{cls.filename}', 'w') as fil:
            json.dump(lst, fil)
        return id

    @classmethod
    def clear(cls):
        with open(f'files/{cls.filename}', 'w') as fil:
            json.dump([], fil)
        return True

    @classmethod
    def get_list(cls) -> list:
        with open(f'files/{cls.filename}', 'r') as fil:
            lst = json.load(fil)
        return lst


class Admins(Users):
    filename = ADMIN_LIST
