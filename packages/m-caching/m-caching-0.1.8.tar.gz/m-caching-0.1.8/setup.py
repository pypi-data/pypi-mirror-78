from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='m-caching',
      version='0.1.8',
      description='Setup normal class to mobio lru cache',
      url='https://github.com/mobiovn',
      author='MOBIO',
      author_email='contact@mobio.vn',
      license='MIT',
      packages=['mobio/libs/caching'],
      install_requires=["redis"],
      long_description=long_description,
      long_description_content_type='text/markdown')
