import sys

# Make sure we are running python3.5+
if 10 * sys.version_info[0]  + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'pyimgconvert',
      version          =   '1.0.8',
      description      =   '(Python) utility which acts as a wrapper around the Linux CLI: convert',
      long_description =   readme(),
      author           =   'FNNDSC',
      author_email     =   'dev@babymri.org',
      url              =   'https://github.com/FNNDSC/pyimgconvert',
      packages         =   ['pyimgconvert'],
      install_requires =   ['pudb'],
      #test_suite       =   'nose.collector',
      #tests_require    =   ['nose'],
      scripts          =   ['bin/pyimgconvert'],
      license          =   'MIT',
      zip_safe         =   False
)