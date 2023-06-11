from markups import inline_keyboards


def test_answer():
    assert inline_keyboards.make_callback_data(2) == inline_keyboards.MenuCD(level='2', category=0, subcategory=0).pack()


class Nnnm:
    a = 0
    def show(self):
        print(self.a)

Nnnm.show