import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'analogcaption'
AUTHOR = 'Analog Teams'
AUTHOR_EMAIL = 'james@analogteams.com'
URL = 'https://bitbucket.org/Lormenyoh/image-caption-generator/src/master/'

LICENSE = 'The MIT License'
DESCRIPTION = 'A Package that uses AI to give users the caption of an image'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'pandas',
    'h5py==2.10.0',
    'idna==2.10',
    'itsdangerous==1.1.0', 
    'Jinja2==2.11.2',
    'Keras==2.2.4',
    'tensorflow>=1.12.1',
    'Keras-Applications==1.0.7',
    'Keras-Preprocessing==1.1.1',
    'Markdown==3.2.2',
    'MarkupSafe==1.1.1',
    'numpy==1.16.1',
    'tensorboard==2.3.0',
    'tensorboard-plugin-wit==1.7.0',
    'tensorflow-estimator==2.3.0',
    'Werkzeug==0.15.5',
    'wrapt==1.12.1'


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