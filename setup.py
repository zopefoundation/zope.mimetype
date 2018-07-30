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

BROWSER_REQUIRES = [
    'zope.browser', # ITerms in source.py
    'zope.browserresource', # metaconfigure for icon in zcml.py
    'zope.formlib>=4.0', # widget.py
    'zope.publisher', # IBrowserRequest
]

TEST_REQUIRES = BROWSER_REQUIRES + [
    'zope.testing',
    'zope.testrunner',
]

setup(name='zope.mimetype',
      version='2.3.2',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description="A simple package for working with MIME content types",
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
      ),
      keywords="file content mimetype",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='https://github.com/zopefoundation/zope.mimetype',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope'],
      extras_require={
          'test': TEST_REQUIRES,
          'browser': BROWSER_REQUIRES,
          'docs': [
              'Sphinx',
              'sphinx_rtd_theme',
              'repoze.sphinx.autointerface',
          ] + BROWSER_REQUIRES,
      },
      install_requires=[
          'setuptools',
          'zope.component',
          'zope.configuration',
          'zope.contenttype>=3.5',
          'zope.event',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
          'zope.security',
      ],
      tests_require=TEST_REQUIRES,
      test_suite='zope.mimetype.tests',
      include_package_data=True,
      zip_safe=False,
)
