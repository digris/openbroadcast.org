#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from djangocms_panel import __version__

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Communications',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='djangocms-panel',
    version=__version__,
    description='Bootstrap panel plugin for Django-CMS',
    author='T. Scott Barnes',
    author_email='barnes.t.scott@gmail.com',
    url='https://github.com/tsbarnes/djangocms-panel',
    packages=['djangocms_panel', 'djangocms_panel.migrations',],
    license='LICENSE.txt',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False
)
