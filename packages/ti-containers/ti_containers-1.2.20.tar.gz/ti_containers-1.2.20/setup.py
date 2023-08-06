# -*- coding: utf8 -*-

from __future__ import absolute_import

from setuptools import setup, find_packages


def read(fname):
    with open(fname, 'r') as file:
        return file.read()


setup(
    name="ti_containers",
    version=read("version").strip(),
    url='https://cloud.tencent.com',
    license="Apache License 2.0",
    description="Open source library for training container on TencentCloud TIONE.",
    long_description=read("README.md"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=['retrying==1.3.3', 'six==1.12.0'],
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': ['train=ti_containers.train:main'],
    },
    author="TencentCloud TIONE",
    keywords="TencentCloud ML TI AI Training",
)
