#!/usr/bin/env python3

import os
from datetime import datetime
from setuptools import setup, find_packages
from sett.__init__ import URL_READTHEDOCS, URL_GITLAB

# 0.0.0-dev.* version identifiers for development only (not public)
__version__ = os.environ.get(
    "CI_COMMIT_TAG", "0.0.0.dev" + os.environ.get("CI_JOB_ID", datetime.now().strftime("%Y%m%d")))

setup(
    name="sett",
    version=__version__,
    license="LGPL3",
    description="Data compression, encryption and transfer tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Robin Engler, Jaroslaw Surkont, Gerhard Bräunlich, Kevin Sayers, Christian Ribeaud",
    author_email="Robin.Engler@sib.swiss, "
    "jaroslaw.surkont@unibas.ch, "
    "gerhard.braeunlich@id.ethz.ch, "
    "sayerskt@gmail.com, "
    "christian.ribeaud@karakun.com",
    url="https://gitlab.com/biomedit/sett",
    install_requires=[
        "gpg-lite>=0.6.13",
        "libbiomedit>=0.2.0",
        "paramiko>=2.7.1",
        "PySide2==5.14.1",
        "dataclasses ; python_version<'3.7'"
    ],
    extras_require={
        "socks":  ["PySocks"]
    },
    packages=find_packages(exclude=["test", "test.*"]),
    package_data={"sett": ["py.typed"]},
    zip_safe=False,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["sett=sett.cli:run"],
        "gui_scripts": ["sett-gui=sett.gui:run"]
    },
    test_suite="test",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Documentation': URL_READTHEDOCS,
        'Source': URL_GITLAB,
    },
)
