import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.3'
PACKAGE_NAME = 'logPoints'
AUTHOR = 'RosiePuddles'
AUTHOR_EMAIL = 'rosiegbartlett@gmail.com'
URL = 'https://github.com/RosiePuddles/log_points'

LICENSE = 'MIT Licence'
DESCRIPTION = 'Adds log points and markers with debug information'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
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
      install_requires=INSTALL_REQUIRES
      )
