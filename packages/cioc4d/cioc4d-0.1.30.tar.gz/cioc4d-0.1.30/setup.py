#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os
import setuptools
from PIL import Image

from setuptools.command.build_py import build_py


NAME = "cioc4d"
DESCRIPTION = "C4D plugin for Conductor Cloud Rendering Platform."
URL = "https://github.com/AtomicConductor/conductor-c4d"
EMAIL = "info@conductortech.com"
AUTHOR = "conductor"
REQUIRES_PYTHON = "~=2.7"
REQUIRED = ["ciocore>=0.2.7,<1.0.0"]
HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

class BuildCommand(build_py):
    def run(self):
        build_py.run(self)

        if not self.dry_run:
            target_dir = os.path.join(self.build_lib, NAME)
            self.write_version_info(target_dir)
            self.convert_icons(target_dir)

    def write_version_info(self, target_dir):
        with open(os.path.join(target_dir, "VERSION"), "w") as f:
            f.write(VERSION)

    def convert_icons(self, target_dir):
        """Convert icons using PIL."""
        out_icon_dir = os.path.join(target_dir, "res")
        icons_dir = os.path.join("images", "icons")
        icon_files = os.listdir(icons_dir)
        for icon_file in icon_files:
            base, ext = os.path.splitext(icon_file)
            icon_path = os.path.join(icons_dir, icon_file)
            size = 30
            icon = Image.open(icon_path)
            icon.thumbnail((size, size), Image.BICUBIC)
            out_icon_file = os.path.join(
                out_icon_dir, "{}_{}x{}{}".format(base, size, size, ext))
            icon.save(out_icon_file)
 
setuptools.setup(
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
    ],
    cmdclass={"build_py": BuildCommand},
    description=DESCRIPTION,
    install_requires=REQUIRED,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    name=NAME,
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    include_package_data=True,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    version=VERSION,
    zip_safe=False,
    package_data={NAME: ["res/*.*", "res/*/*.*", "res/*/*/*.*", "Conductor.pyp", ]}
)
