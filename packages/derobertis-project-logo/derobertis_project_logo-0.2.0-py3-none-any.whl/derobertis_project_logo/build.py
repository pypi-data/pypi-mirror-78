import os
from typing import Sequence

from derobertis_project_logo.creations import LOGOS
from derobertis_project_logo.project_logo import ProjectLogo


def build_logos(logos: Sequence[ProjectLogo] = LOGOS, out_folder: str = '.'):
    for logo in logos:
        out_path = os.path.join(out_folder, logo.name + '.svg')
        logo.logo.render(out_path)


def build_rst(logos: Sequence[ProjectLogo] = LOGOS, out_folder: str = '.', images_folder: str = '.'):
    out_path = os.path.join(out_folder, 'creations.rst')
    rst = "Created Logos\n*****************"
    for logo in logos:
        rst += '\n'
        rst += logo.rst(images_folder)
    with open(out_path, 'w') as f:
        f.write(rst)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('images_folder', default='.')
    parser.add_argument('rst_folder', default='.')
    args = parser.parse_args()

    if not os.path.exists(args.images_folder):
        os.makedirs(args.images_folder)

    images_relative_folder = os.sep.join(args.images_folder.split(os.sep)[2:])

    build_logos(out_folder=args.images_folder)
    build_rst(out_folder=args.rst_folder, images_folder=images_relative_folder)
