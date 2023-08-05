# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='LogCollectionFormatter',
    version='1.1.0',
    description=('A python log handler format log messages and records them by loggin module'),
    author='Licong',
    author_email='17601072928@sina.cn',
    license='MIT',
    packages=find_packages(),
    platforms=['all'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='log collection formatter includes debug, info, error, warn, external, internal functions to formats and records log message',
    install_requires=[
    ],
)
