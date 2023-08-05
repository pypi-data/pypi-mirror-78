#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File : setup.py
@Author : Braylon1002
@Version : 1.0
@Contact : S.Braylon1002@gmail.com
Desc : None
"""

from setuptools import setup, find_packages

setup(
    name='featureColByTorch',
    version=1.0,
    description=(
        'this is a feature column and transformer tools in pytorch, which is like the featureColumn class in Tensorflow'
    ),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Braylon',
    author_email='S.Braylon1002@gmail.com',
    maintainer='Braylon',
    maintainer_email='S.Braylon1002@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url="https://blog.csdn.net/qq_40742298",
    install_requires=[
        'numpy',
        'pandas',
    ],
)
