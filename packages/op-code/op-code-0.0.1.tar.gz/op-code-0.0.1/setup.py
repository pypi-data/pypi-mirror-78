from setuptools import setup
from setuptools import find_packages

import pathlib

path = pathlib.Path(__file__).parent.resolve()

ld = (path / 'README.md').read_text(encoding = 'utf-8')

setup(
    name = 'op-code',
    author = 'Phoxett',
    author_email = 'phoxett@gmail.com',
    maintainer = 'Phoxett',
    maintainer_email = 'phoxett@gmail.com',
    version = '0.0.1',
    url = 'https://phoxett.github.io/op-code/',
    package_dir = {'':'src'},
    packages = find_packages(where = 'src'),
    description = 'Phoxett OP codec library for scientific solutions',
    long_description = ld,
    long_description_content_type = 'text/markdown',
    )