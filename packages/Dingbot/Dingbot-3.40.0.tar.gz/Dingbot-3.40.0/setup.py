#!/usr/bin/env python
# coding=utf-8

from setuptools import setup
import dingbot

setup(
    name='Dingbot',
    version=dingbot.__version__,
    description=('a Dingtalk group robot\'s API by python'),
    long_description=open('README.txt').read(),
    author='Wu Junkai',
    author_email='wujunkai20041123@outlook.com',
    license='BSD License',
    packages=[],
    py_modules= ['dingbot'],
    platforms=["all"],
    url='https://github.com/WuJunkai2004/Dingbot',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
