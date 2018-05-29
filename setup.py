#!/usr/bin/env python3
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='charpe',
    description='Sends messages from applications through different media',
    long_description=long_description,
    url='https://github.com/tracsa/charpe',

    version='1.0.0',

    author='Abraham Toriz Cruz',
    author_email='categulario@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='notification',

    packages=[
        'charpe',
    ],

    package_data={'charpe': ['templates/**']},

    entry_points={
        'console_scripts': [
            'charped = charpe.main:main',
        ],
    },

    include_package_data=True,

    install_requires=[
        'jinja2',
        'simplejson',
        'requests',
        'pika',
        'itacate',
        'pytz',
        'case_conversion',
    ],

    setup_requires=[
        'pytest-runner',
    ],

    tests_require=[
        'pytest',
        'pytest-mock',
    ],
)
