#!/usr/bin/env python
from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    version='0.0.2',
    name='samsgeneratechangelog',
    packages=['samsgeneratechangelog'],
    description='Let Sam generate a changelog for you by grouping commits by file, or commit message, or anything!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sam Martin', 
    author_email='samjackmartin+sams_generate_changelog@gmail.com', 
    url='https://github.com/Sam-Martin/sams-generate-changelog',
    project_urls={
        "Documentation": "https://sams-generate-changelog.readthedocs.io/en/latest/"
    },
    install_requires=['jinja2', 'configargparse', 'gitpython'],
    package_data={
        "": ["templates/*.j2"],
    },
    entry_points={
        'console_scripts': ['sgc=samsgeneratechangelog.__main__:main']
    }

)