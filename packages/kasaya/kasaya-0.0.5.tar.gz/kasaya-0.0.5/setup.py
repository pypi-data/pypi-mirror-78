from setuptools import setup, dist, find_packages
from setuptools.command.install import install
import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(PROJECT_DIR, 'README.md')) as f:
    long_description = f.read()

setup(
    name='kasaya',
    version='0.0.5',
    packages=find_packages(),
    license='MIT',
    description="A tool to juice information from URL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'lxml==4.5.2',
        'requests==2.22.0',
        'beautifulsoup4==4.9.1',
        'dnspython==2.0.0',
        'sphinx==3.1.2'
    ],
    url='http://github.com/git-kale/kasaya',
    author='Mahesh Kale',
    author_email='kalemaheshj@gmail.com',
    options={'bdist_wheel': {'universal': '1'}}
)