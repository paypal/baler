#!/usr/bin/env python

import os

from setuptools import setup, find_packages

long_description = 'Baler is a tool that makes it easy to bundle and use resources (images, strings files, etc.) in a compiled static library.'
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

if os.path.exists('LICENSE'):
    license = open('LICENSE').read()

setup(name='baler',
      version='1.0.3',
      description='Bundle assets into iOS static libraries',
      long_description=long_description,
      keywords=['ios', 'objective-c', 'generation', 'static', 'resource', 'NSBundle', 'mobile'],
      author='PayPal SDK Team',
      author_email='brfitzgerald@paypal.com, jbleechersnyder@paypal.com',
      url='https://github.com/paypal/baler',
      scripts=['bale'],
      packages=find_packages(),
      package_dir={'baler': 'baler'},
      package_data={'baler': ['templates/*.j2']},
      license=license,
      install_requires=[
          'Jinja2 >= 2.6',
          'argparse >= 1.1',
          'biplist >= 0.5',
          'six >= 1.2.0',
          'wsgiref >= 0.1.2',
      ])
