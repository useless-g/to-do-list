from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='to_do_list',
    version='0.0.1',
    packages=find_packages(),
    author='Sergeus',
    author_email='uzellessmovic@gmail.com',
    description='todo list',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=open(join(dirname(__file__), 'requirements.txt')).read().split('\n'),
)
