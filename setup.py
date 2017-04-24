##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.mimetype package
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

setup(name='zope.mimetype',
      version='2.2.0',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description = "A simple package for working with MIME content types",
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'README.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'retrieving_mime_types.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'codec.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'constraints.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'contentinfo.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'event.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'typegetter.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'source.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'widget.txt')
          + '\n\n' +
          read('src', 'zope', 'mimetype', 'utils.txt')
          + '\n\n' +
          read('CHANGES.rst')
          ),
      keywords = "file content mimetype",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.mimetype',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      extras_require = dict(
        test=[
            'zope.component',
            'zope.testing',
            ]
        ),
      install_requires=['setuptools',
                        'zope.browser',
                        'zope.browserresource',
                        'zope.component',
                        'zope.configuration',
                        'zope.contenttype>=3.5',
                        'zope.event',
                        'zope.formlib>=4.0',
                        'zope.i18n',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.publisher',
                        'zope.schema',
                        'zope.security',
                        ],
      tests_require=[
            'zope.component',
            'zope.testing',
            ],
      test_suite='zope.mimetype.tests',
      include_package_data = True,
      zip_safe = False,
      )
