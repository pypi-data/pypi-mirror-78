from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='distributions_gb001',
      version='1.0',
      description='Gaussian and binomial distributions',
      packages=['distributions_gb001'],
      author="Abeeb Ridwan Olumide",
      author_email="olumideuae@gmail.com",
      setup_requires=['wheel'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
