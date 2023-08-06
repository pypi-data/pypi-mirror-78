import pathlib
import sys

from bokeh.events import Event


ROOT_PATH = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_PATH))

from typing import Type

import panel as pn
import param
from panel.viewable import Viewable

from derobertis_project_logo.logo import Logo
from derobertis_project_logo.logos.main import LOGO_CLASSES


class LogoModel(param.Parameterized):
    klass: Type[Logo] = param.ObjectSelector(objects=LOGO_CLASSES)
    instance: Logo = param.ClassSelector(class_=Logo)
    project_name: str = param.String(default='my_project')

    def __init__(self, **params):
        if 'klass' not in params:
            params['klass'] = LOGO_CLASSES[0]
        if 'instance' not in params:
            klass = params['klass']
            logo = klass()
            logo.set_random_colors()
            params['instance'] = logo
        super().__init__(**params)

    def _repr_svg_(self) -> str:
        return self.instance.render_str()

    def _set_instance(self):
        logo = self.klass()
        logo.set_random_colors()
        self.instance = logo


def get_view() -> Viewable:
    logo_model = LogoModel()
    svg = pn.pane.SVG(object=logo_model)
    editor = pn.widgets.Ace(
        value=logo_model.instance.to_definition(logo_model.project_name),
        width=500
    )

    def randomize_color(event: Event):
        logo_model.instance.set_random_colors()
        svg.object = logo_model
        editor.value = logo_model.instance.to_definition(logo_model.project_name)

    def randomize_and_set_instance(event: Event):
        logo_model._set_instance()
        randomize_color(event)

    random_colors_button = pn.widgets.Button(name='Randomize Colors')
    random_colors_button.on_click(randomize_color)
    logo_model.param.watch(randomize_and_set_instance, ['klass'])

    return pn.Column(
        pn.Row(logo_model.param, editor),
        random_colors_button,
        svg
    )

get_view().servable()