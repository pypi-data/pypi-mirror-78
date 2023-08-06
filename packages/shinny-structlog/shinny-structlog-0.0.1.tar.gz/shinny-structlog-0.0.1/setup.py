# -*- coding: utf-8 -*-
__author__ = 'mayanqiong'

import setuptools

setuptools.setup(
    name='shinny-structlog',
    version="0.0.1",
    url='https://github.com/shinnytech/structlog-python',
    packages=['shinny_structlog'],
    description='Shinny StructLog',
    author='TianQin',
    author_email='tianqincn@gmail.com',
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
    ],
)
