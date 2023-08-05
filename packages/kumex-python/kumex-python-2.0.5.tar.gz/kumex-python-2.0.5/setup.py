#!/usr/bin/python
# -*- coding:utf-8 -*-

from setuptools import setup


setup(
    name='kumex-python',
    version='v2.0.5',
    packages=['kumex', 'kumex/base_request', 'kumex/marke_data', 'kumex/trade', 'kumex/user',
              'kumex/websocket', 'kumex/ws_token'],
    license="MIT",
    author='Grape',
    author_email="grape.zhang@kucoin.com",
    url='https://github.com/Kucoin/kumex-python-sdk',
    description="kumex-api-sdk",
    install_requires=['requests', 'websockets'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
