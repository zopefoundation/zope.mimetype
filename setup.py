##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Setup for zope.mimetype package

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.1.1'

setup(name='zope.mimetype',
      version=version,
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description = "A simple package for working with MIME content types",
      long_description=(
          read('README.txt')
          + '\n\n' +
          '.. contents::'
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
          read('CHANGES.txt')
          ),
      keywords = "file content mimetype",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
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
          test=['zope.app.securitypolicy',
                'zope.app.testing',
                'zope.app.zcmlfiles',
                'zope.securitypolicy',
                ]),
      install_requires=['setuptools',
                        'zope.component',
                        'zope.configuration',
                        'zope.interface',
                        ],
      include_package_data = True,
      zip_safe = False,
      )
