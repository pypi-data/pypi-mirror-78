import sys
if sys.version_info < (3,0):
    sys.exit('Sorry, Python 2 is not supported')

from setuptools import setup, find_packages
from pyrealtime import __version__


setup(
    name="PyRealtime",
    version=__version__,
    packages=find_packages(),
    description='A package for realtime data processing, including reading from serial ports and plotting.',
    author='Eric Whitmire',
    author_email='emwhit@cs.washington.edu',
    url='https://github.com/ewhitmire/pyrealtime',
    keywords=['realtime', 'plotting', 'serialport', 'logging', 'pipeline'],
    test_suite='nose.collector',
    install_requires=[
       'numpy',
       'matplotlib'
    ]
)
