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

import doctest
import unittest

from zope.component import testing


def optional_test_suite_setUp(required_module):

    def setUp(test):
        import importlib
        try:
            importlib.import_module(required_module)
        except ModuleNotFoundError:  # pragma: no cover
            raise unittest.SkipTest(
                "Required module %r missing" %
                (required_module,))
        testing.setUp(test)
    return setUp


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            '../retrieving_mime_types.rst',
            setUp=testing.setUp, tearDown=testing.tearDown),
        doctest.DocFileSuite(
            '../event.rst',
            setUp=testing.setUp, tearDown=testing.tearDown),
        doctest.DocFileSuite(
            '../source.rst',
            setUp=optional_test_suite_setUp('zope.browser'),
            tearDown=testing.tearDown),
        doctest.DocFileSuite(
            '../constraints.rst'),
        doctest.DocFileSuite(
            '../contentinfo.rst',
            setUp=testing.setUp, tearDown=testing.tearDown),
        doctest.DocFileSuite(
            '../typegetter.rst'),
        doctest.DocFileSuite(
            '../utils.rst'),
        doctest.DocFileSuite(
            '../widget.rst',
            setUp=optional_test_suite_setUp('zope.publisher'),
            tearDown=testing.tearDown),
        doctest.DocFileSuite(
            '../codec.rst',
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        ),
        doctest.DocFileSuite(
            '../configure.rst',
            setUp=testing.setUp, tearDown=testing.tearDown,
        ),
    ))
