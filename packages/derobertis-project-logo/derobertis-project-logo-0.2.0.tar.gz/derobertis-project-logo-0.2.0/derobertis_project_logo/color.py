import random

from colour import Color as LibColor


class Color(LibColor):

    def to_definition(self):
        return f'Color("{self.get_hex()}")'


def random_color_hex() -> str:
    return Color(pick_for=random.randint(1, 1000000)).get_hex()
