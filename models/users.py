import json


class Users:
    filename = 'user_list.txt'

    def add(id, filename=filename):
        with open(f'files/{filename}', 'r') as fil:
            lst = json.load(fil)
        lst.append(id)
        with open(f'files/{filename}', 'w') as fil:
            json.dump(lst, fil)
        return id

    def remove(id, filename=filename):
        with open(f'files/{filename}', 'r') as fil:
            lst = json.load(fil)
        lst.remove(id)
        with open(f'files/{filename}', 'w') as fil:
            json.dump(lst, fil)
        return id

    def clear(filename=filename):
        with open(f'files/{filename}', 'w') as fil:
            json.dump([], fil)
        return True

    def get_list(filename=filename) -> list:
        with open(f'files/{filename}', 'r') as fil:
            lst = json.load(fil)
        return lst


class Admins:
    filename = 'admin_list.txt'

    def add(id, filename=filename):
        with open(f'files/{filename}', 'r') as fil:
            lst = json.load(fil)
        lst.append(id)
        with open(f'files/{filename}', 'w') as fil:
            json.dump(lst, fil)
        return id

    def remove(id, filename=filename):
        with open(f'files/{filename}', 'r') as fil:
            lst = json.load(fil)
        lst.remove(id)
        with open(f'files/{filename}', 'w') as fil:
            json.dump(lst, fil)
        return id

    def clear(id, filename=filename):
        with open(f'files/{filename}', 'w') as fil:
            json.dump([id], fil)
        return True

    def get_list(filename=filename) -> list:
        with open(f'files/{filename}', 'r') as fil:
            lst = json.load(fil)
        return lst
