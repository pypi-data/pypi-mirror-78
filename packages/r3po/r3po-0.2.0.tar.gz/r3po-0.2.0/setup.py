import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.2.0'
PACKAGE_NAME = 'r3po'
AUTHOR = 'Zhenghong Lieu'
AUTHOR_EMAIL = 'lieuzhenghong@email.com'
URL = 'https://github.com/lieuzhenghong/r3po'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'A library built on top of Ray to make embarassingly parallel tasks embarassingly easy'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'ray>=0.8.7',
    'pyyaml>=5.3.1',
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
