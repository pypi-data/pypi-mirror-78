from setuptools import setup, find_packages

setup(
    name = 'oye_vix',# while installing pacakge
    version = '0.0.1',
    description = 'This has custom functions.',
    long_description = open('Readme.txt').read(),
    url = 'https://github.com/imvickykumar999',
    author = 'Vicky Kumar',
    keywords = ['custom','python package','function and class'],
    license = 'MIT',
    packages = ['oye_vix'],# while importing package
    install_requires = ['']
)