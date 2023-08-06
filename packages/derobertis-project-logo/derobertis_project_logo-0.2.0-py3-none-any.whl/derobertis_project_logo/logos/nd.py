from derobertis_project_logo.logo import Logo
from derobertis_project_logo.shape import Shape


class ND(Logo):

    def __init__(self):
        shapes = [
            Shape('background'),
            Shape('foreground'),
        ]
        super().__init__('nd', shapes)
