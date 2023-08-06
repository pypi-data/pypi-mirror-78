from setuptools import setup, find_packages
from os.path import join, dirname
import openMystatAPI

setup(
    name='openMystatAPI',
    version=openMystatAPI.__version__,
    author='Vezono',
    author_email='gbball.baas@gmail.com',
    description='Unofficial, but open API realisation on python of mystat.itstep.org, a site for students of ITSTEP.',
    long_description=open(join(dirname(__file__), 'README.md'), encoding='utf-8').read(),
    url='https://github.com/Vezono/python-mystat-api',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)