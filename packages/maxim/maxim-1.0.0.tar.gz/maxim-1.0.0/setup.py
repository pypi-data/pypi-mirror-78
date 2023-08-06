from setuptools import setup, find_packages

# read the contents of your README file
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="maxim",
    version="1.0.0",
    author="so07",
    author_email="so07@mail.com",
    description="A simple description of maxim project",
    long_description=long_description,
    url="https://github.com/so07/docs",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "argparse",
        "fortune",
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        "bumpversion",
    ],
    entry_points = {
        "console_scripts": [
            "maxim=maxim.maxim:main",
        ],
    },
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
)
