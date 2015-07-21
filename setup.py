#!/usr/bin/env python

from distutils.core import setup

setup(
    name='djwebtools',
    version='0.1',
    author='Fabian Sinz & Edgar Walker',
    author_email='sinz@bcm.edu',
    description='Collection of Flask tools for datajoint. ',
    # url='https://github.com/datajoint/datajoint-python',
    packages=['djwebtools'],
    requires=['numpy', 'datajoint', 'flask','wtforms'],
    license = "MIT",
)
