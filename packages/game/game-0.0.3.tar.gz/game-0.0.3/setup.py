# -*- coding: utf-8 -*-
# @author: leesoar
# @email: secure@tom.com
# @email2: employ@aliyun.com

import io
import os
from setuptools import setup


def read_file(filename):
    with open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


NAME = 'game'
FOLDER = 'game'
DESCRIPTION = 'A web game emulator, not only can play games. Welcome to explore.'
URL = 'https://leesoar.com'
EMAIL = 'secure@tom.com'
AUTHOR = 'leesoar'
REQUIRES_PYTHON = '>=3.3.0'

REQUIRED = read_requirements('requirements.txt')

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setup(
    name=NAME,
    version="0.0.3",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=['game'],
    package_data={'game': ['static/*', 'ui_*.jpg']},
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    entry_points={
        'console_scripts': ['game = game.web:run']
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    keywords=[
        'game', 'fc', 'nes', 'emulator', 'nintendo', 'contra'
    ],
)
