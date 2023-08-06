from setuptools import setup, find_packages

setup(name='requests_wrapper',
      version="0.0.1",
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
