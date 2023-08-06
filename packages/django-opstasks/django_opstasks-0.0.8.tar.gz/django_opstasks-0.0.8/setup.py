#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import setuptools
import setuptools.command.test

VERSION = '0.0.8'

NAME = 'django_opstasks'

PACKAGES = setuptools.find_packages(include=(
    'django_opstasks',
    'django_opstasks.common',
    'django_opstasks.backends',
    'django_opstasks.migrations'
))

CLASSES = """
    Development Status :: 1 - Planning
    License :: OSI Approved :: BSD License
    Programming Language :: Python
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Framework :: Django
    Framework :: Django :: 3.0
    Operating System :: OS Independent
    Topic :: Communications
    Topic :: System :: Distributed Computing
    Topic :: Software Development :: Libraries :: Python Modules
"""
classifiers = [s.strip() for s in CLASSES.split('\n') if s]


if sys.version_info < (3, 6):
    raise Exception(f'{NAME} {VERSION} requires Python 3.6 or later!')

with open("PYPI.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    version=VERSION,
    name=NAME,
    packages=PACKAGES,
    description='opstasks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='opstasks',
    author='lunuan',
    author_email='admin@lunuan.com.cn',
    url='',
    platforms=['any'],
    license='BSD',
    classifiers=classifiers,
    install_requires='celery>=4.4,<5.0',
    # tests_require=reqs('test.txt') + reqs('test-django.txt'),
    # cmdclass={'test': pytest},
    entry_points={
        'celery.result_backends': [
            'opstasks-backends = django_opstasks.backends:DatabaseBackend',
            'opstasks-cache = django_opstasks.backends:CacheBackend',
        ],
    },
    zip_safe=False,
    include_package_data=False,
)
