from typing import Optional

from derobertis_project_logo.color import Color


class Shape:

    def __init__(self, name: str, color: Optional[Color] = None):
        self.name = name
        self.color = color
