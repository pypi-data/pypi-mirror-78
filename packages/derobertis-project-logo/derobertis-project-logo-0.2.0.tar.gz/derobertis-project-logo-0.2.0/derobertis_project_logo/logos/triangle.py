from derobertis_project_logo.color import Color
from derobertis_project_logo.logo import Logo
from derobertis_project_logo.shape import Shape


class Triangle(Logo):

    def __init__(self):
        shape_names = [f'{i + 1}' for i in range(12)]
        shapes = [Shape(name) for name in shape_names]
        shapes.append(Shape('border', Color('black')))
        super().__init__('triangle', shapes)

    def set_random_colors(self):
        shapes = [shape for shape in self.shapes if shape.name != 'border']
        self._set_random_colors(shapes)
