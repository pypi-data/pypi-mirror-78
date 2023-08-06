#!/usr/bin/env python

"""apu: Antons Python Utilities."""

# Third party
from setuptools import setup

requires_datetime = ["pytz"]
requires_setup = ["GitPython"]
requires_geographie = ["numpy"]
requires_all = (
    requires_datetime
    + requires_setup
    + requires_geographie
)

setup(
    version="0.1.5",
    package_data={"apu": []},
    project_urls={
        'Documentation': 'https://afeldman.github.io/apu/',
        'Source': 'https://github.com/afeldman/apu',
        'Tracker': 'https://github.com/afeldman/apu/issues',
    },
    extras_require={
        "all": requires_all,
        "datetime": requires_datetime,
        "setup": requires_setup,
        "geo": requires_geographie,
    },
)