#!/usr/bin/env python
import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    install_requires = [line.rstrip('\r\n') for line in file]

setuptools.setup(
  name = 'connectedcarscomm',
  version = '0.1.0',
  author = 'Jais Heslegrave',
  author_email = 'heslegrave@gmail.com',
  description = 'Simple communication library for ConnectedCars.io',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/heslegrave/connectedcarscomm',
  keywords = ['ConnectedCars', 'Audi', 'Volkswagen', 'Skoda', 'SEAT'],
  packages = setuptools.find_packages(),
  classifiers = [
    'Programming Language :: Python :: 3.7',
    "License :: OSI Approved :: MIT License",
  ],
  python_requires='>=3.7',
)
