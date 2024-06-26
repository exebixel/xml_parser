from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='xml_parser_comp',
    version='1.0',
    description='A simple XML parser component',
    author='Exebixel',
    author_email='ezequielnat7@gmail.com',
    packages=find_packages(),
    install_requires=requirements,
)