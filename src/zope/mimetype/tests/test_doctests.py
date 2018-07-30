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

def optional_test_suite_setUp(required_module):

    def setUp(test):
        import importlib
        try:
            importlib.import_module(required_module)
        except ImportError: # pragma: no cover
            raise unittest.SkipTest("Required module %r missing" % (required_module,))
        testing.setUp(test)
    return setUp

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            '../retrieving_mime_types.rst',
            setUp=testing.setUp, tearDown=testing.tearDown,
            checker=checker),
        doctest.DocFileSuite(
            '../event.rst',
            setUp=testing.setUp, tearDown=testing.tearDown,
            globs={'print_function': print_function},
            checker=checker),
        doctest.DocFileSuite(
            '../source.rst',
            setUp=optional_test_suite_setUp('zope.browser'), tearDown=testing.tearDown,
            checker=checker),
        doctest.DocFileSuite(
            '../constraints.rst',
            checker=checker),
        doctest.DocFileSuite(
            '../contentinfo.rst',
            setUp=testing.setUp, tearDown=testing.tearDown,
            checker=checker),
        doctest.DocFileSuite(
            '../typegetter.rst',
            checker=checker),
        doctest.DocFileSuite(
            '../utils.rst',
            checker=checker),
        doctest.DocFileSuite(
            '../widget.rst',
            setUp=optional_test_suite_setUp('zope.publisher'), tearDown=testing.tearDown,
            checker=checker),
        doctest.DocFileSuite(
            '../codec.rst',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=checker,
        ),
        doctest.DocFileSuite(
            '../configure.rst',
            setUp=testing.setUp, tearDown=testing.tearDown,
            checker=checker
        ),
    ))


additional_tests = test_suite # for 'python setup.py test'

if __name__ == '__main__': # pragma: no cover
    unittest.main(defaultTest='test_suite')
