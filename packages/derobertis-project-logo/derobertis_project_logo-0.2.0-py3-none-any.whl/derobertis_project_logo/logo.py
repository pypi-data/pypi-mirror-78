import pathlib
from typing import Sequence, Dict, Any, Optional

from jinja2 import Environment, FileSystemLoader, Template

from derobertis_project_logo.color import random_color_hex, Color
from derobertis_project_logo.shape import Shape

TEMPLATE_DIR = pathlib.Path(__file__).parent / 'templates'
jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))


class Logo:
    """
    The base class for logo images
    """

    def __init__(self, template_name: str, shapes: Sequence[Shape]):
        self.template_name = template_name
        self.shapes = shapes

    def set_color(self, shape_name: str, color: str):
        shape = self.shapes_by_name[shape_name]
        color_obj = Color(color)
        shape.color = color_obj

    def set_random_colors(self):
        self._set_random_colors()

    def _set_random_colors(self, shapes: Optional[Sequence[Shape]] = None):
        if shapes is None:
            shapes = self.shapes

        for shape in shapes:
            shape.color = Color(random_color_hex())

    @property
    def shapes_by_name(self) -> Dict[str, Shape]:
        return {shape.name: shape for shape in self.shapes}

    @property
    def render_dict(self) -> Dict[str, Any]:
        colors = {
            f'color_{shape.name}': shape.color.get_hex() if shape.color is not None else None
            for shape in self.shapes
        }
        all_variables = {
            **colors,
        }
        return all_variables

    @property
    def template(self) -> Template:
        return jinja_env.get_template(f'{self.template_name}.svg.j2')

    def render_str(self, extra_variables: Optional[Dict[str, Any]] = None) -> str:
        if extra_variables is None:
            extra_variables = {}

        all_data = {**self.render_dict, **extra_variables}
        return self.template.render(**all_data)

    def render(self, out_path: str = 'logo.svg', extra_variables: Optional[Dict[str, Any]] = None):
        rendered = self.render_str(extra_variables)
        with open(out_path, 'w') as f:
            f.write(rendered)

    def color_definition(self, project_name: str):
        variable_name = f'_{project_name}_logo'
        return '\n'.join([
            f'{variable_name}.set_color("{shape.name}", "{shape.color.get_hex()}")'
            if shape.color else '' for shape in self.shapes
        ])

    def to_definition(self, project_name: str) -> str:
        variable_name = f'_{project_name}_logo'
        parts = [
            f'{variable_name} = {self.__class__.__name__}()',
            self.color_definition(project_name),
            f'{project_name}_logo = ProjectLogo("{project_name}", {variable_name})'
        ]
        return '\n'.join(parts)
