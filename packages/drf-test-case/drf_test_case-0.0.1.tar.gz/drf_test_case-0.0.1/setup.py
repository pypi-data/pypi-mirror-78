# -*- coding:utf-8 -*-

from setuptools import setup
from setuptools import find_packages
from drf_test_case import __version__

setup(
    name='drf_test_case',
    description='using python code to communicate with aws client',
    long_description='',
    classifiers=[],
    keywords='',
    author='Lawes',
    author_email='haiou_chen@sina.cn',
    url='https://github.com/MrLawes/drf_test_case',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'djangorestframework>=3.8.2',
        'Django>=2.0.9',
    ],
    version=__version__,
)
