from os import path
from setuptools import setup, find_packages

from requests_wrapper import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='requests_wrapper',
      long_description=long_description,
      long_description_content_type='text/markdown',
      version=__version__,
      author="E CHOW",
      author_email="chilledgeek@gmail.com",
      description='Wrapper around requests package, with extra API key management',
      url="https://github.com/chilledgeek/requests-wrapper",
      packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
      license="MIT",
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ],
      install_requires=['requests'])
