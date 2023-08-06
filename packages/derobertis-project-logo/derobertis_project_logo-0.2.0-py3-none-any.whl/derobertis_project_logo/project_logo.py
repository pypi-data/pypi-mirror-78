import os

from derobertis_project_logo.logo import Logo


class ProjectLogo:

    def __init__(self, name: str, logo: Logo):
        self.name = name
        self.logo = logo

    def rst(self, images_folder: str, width: float = 700):
        image_path = os.path.join(images_folder, f'{self.name}.svg')
        rst = f"""
{self.name} Logo
============================================================================

.. image:: {image_path}
    :width: {width}
    :alt: Logo for {self.name}
        """.strip()
        return rst
