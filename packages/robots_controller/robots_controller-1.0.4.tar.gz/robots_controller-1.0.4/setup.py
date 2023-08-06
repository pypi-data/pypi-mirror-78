import io
import os
import re
import sys

from setuptools import setup

PATH_BASE = os.path.dirname(__file__)


def read_file(fpath):
    """Reads a file within package directories."""
    with io.open(os.path.join(PATH_BASE, fpath)) as f:
        return f.read()

def get_version():
    """Returns version number, without module import (which can lead to ImportError
    if some dependencies are unavailable before install."""
    contents = read_file(os.path.join('robots_controller', '__init__.py'))
    version = re.search('VERSION = \(([^)]+)\)', contents)
    version = version.group(1).replace(', ', '.').strip()

    print("*******************")
    print(version)
    print("*******************")
    return version


setup(
    name='robots_controller',
    version=get_version(),
    #version="0.0.3",
    url='https://gitlab.com/SamSafonov/robots_controller',
    license='BSD 1',

    description='Smart robots controller 1',
    long_description=read_file('README.rst'),

    author='Semyon Safonov',
    author_email='samsaf@gmail.com',

    packages=['robots_controller'],
    include_package_data=True,
    zip_safe=False,

    #setup_requires=['wheel', 'pytest-runner'] if 'test' in sys.argv else [],
    setup_requires=['wheel', 'pytest-runner'],
    test_require=['pytest'],
    install_require=[
        'requests',
        'click',
        'jinja2<3.0'
    ],
    entry_points={
        'console_scripts':['robots_controller = robots_controller.cli.main'],
    },

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=listclassifiers
        #'Development Status :: 5 - Production/Stable',
        #'License :: OSI Approved :: BSD License',
        #'Operation System :: OS Independent',
        #'Programming Langiage :: Python',
        #'Programming Langiage :: Python :: 3.6'
    ],
)


