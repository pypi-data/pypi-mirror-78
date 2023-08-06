#!/usr/bin/env python
from distutils.core import setup

setup(name='ebook-blackener',
    version='0.1.0',
    py_modules=['ebook_blackener'],
    scripts=['ebook-blackener'],

    python_requires='>=3.6',
    install_requires=[
        'cssutils>=1.0.2',
        'docopt>=0.6.2',
    ],

    description="Script / library to set ebooks' texts as white over a black background.",
    author='Millian Poquet',
    author_email='millian.poquet@gmail.com',
    url='https://github.com/mpoquet/ebook-blackener/',
    license='GPL-3.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
