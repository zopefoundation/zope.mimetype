##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test harness for `zope.mimetype` doctests..
"""
from __future__ import print_function

import doctest
import re
import unittest

from zope.component import testing
from zope.testing import renormalizing

checker = renormalizing.RENormalizing([
    # Python 3 unicode removed the "u".
    (re.compile("u('.*?')"),
     r"\1"),
    (re.compile('u(".*?")'),
     r"\1"),
    # Python 3 bytes adds the "b".
    (re.compile("b('.*?')"),
     r"\1"),
    (re.compile('b(".*?")'),
     r"\1"),
    # Python 3 renames builtins.
    (re.compile("__builtin__"),
     r"builtins"),
    ])


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
                '../retrieving_mime_types.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker),
        doctest.DocFileSuite(
                '../event.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                globs={'print_function': print_function},
                checker=checker),
        doctest.DocFileSuite(
                '../source.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker),
        doctest.DocFileSuite(
                '../constraints.txt',
                checker=checker),
        doctest.DocFileSuite(
                '../contentinfo.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker),
        doctest.DocFileSuite(
                '../typegetter.txt',
                checker=checker),
        doctest.DocFileSuite(
                '../utils.txt',
                checker=checker),
        doctest.DocFileSuite(
                '../widget.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker),
        doctest.DocFileSuite(
                '../codec.txt',
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                checker=checker,
        ),
        doctest.DocFileSuite(
                '../configure.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker
        ),
    ))


additional_tests = test_suite # for 'python setup.py test'

if __name__ == '__main__': # pragma: no cover
    unittest.main(defaultTest='test_suite')
