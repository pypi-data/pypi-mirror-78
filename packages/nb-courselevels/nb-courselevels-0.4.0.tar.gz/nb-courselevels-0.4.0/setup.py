#!/usr/bin/env python

import setuptools
from pathlib import Path

VERSION_FILE = Path(__file__).parent / "courselevels" / "version.py"
ENV = {}
with VERSION_FILE.open() as f:
    exec(f.read(), ENV)                                 # pylint: disable=w0122
__version__ = ENV['__version__']


with open("README.md") as feed:
    LONG_DESCRIPTION = feed.read()

setuptools.setup(
    name="nb-courselevels",
    description="Jupyter nbextension to outline 3 course levels through colors",
    version=__version__,
    author="Thierry Parmentelat",
    author_email="thierry.parmentelat@inria.fr",
    long_description=LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    project_urls={
        'source': 'https://github.com/parmentelat/nb-courselevels',
#        'documentation': 'http://nb-courselevels.readthedocs.io/',
    },
    include_package_data=True,
    packages=['courselevels'],
    install_requires=[
        'notebook', 'jupyter_nbextensions_configurator'
    ],
    data_files=[
        # like `jupyter nbextension install --sys-prefix`
        ("share/jupyter/nbextensions/courselevels", [
            "courselevels/static/index.js", "courselevels/static/courselevels.yaml"
        ]),
        # like `jupyter nbextension enable --sys-prefix`
        ("etc/jupyter/nbconfig/notebook.d", [
            "jupyter-config/nbconfig/notebook.d/nb-courselevels.json"
        ])
    ],
    zip_safe=False
)
