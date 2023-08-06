import pytest

from derobertis_project_logo.logos.main import LOGO_CLASSES


@pytest.mark.parametrize('LogoClass', LOGO_CLASSES)
def test_generate_logo(LogoClass):
    logo = LogoClass()
    logo.set_random_colors()
    logo.render()

