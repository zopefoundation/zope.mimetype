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
"""Test harness for `zope.mimetype`.
"""
from __future__ import print_function
import doctest
import re
import unittest

import zope.interface
import zope.mimetype.interfaces
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

class ISampleContentTypeOne(zope.interface.Interface):
    """This is a sample content type interface."""
ISampleContentTypeOne.setTaggedValue("title", u"Type One")
ISampleContentTypeOne.setTaggedValue("extensions", [])
ISampleContentTypeOne.setTaggedValue("mimeTypes", ["type/one", "type/foo"])

zope.interface.directlyProvides(
    ISampleContentTypeOne,
    zope.mimetype.interfaces.IContentTypeInterface)

class ISampleContentTypeTwo(zope.interface.Interface):
    """This is a sample content type interface."""
ISampleContentTypeTwo.setTaggedValue("title", u"Type Two")
ISampleContentTypeTwo.setTaggedValue("mimeTypes", [".ct2", ".ct3"])
ISampleContentTypeTwo.setTaggedValue("mimeTypes", ["type/two"])

zope.interface.directlyProvides(
    ISampleContentTypeTwo,
    zope.mimetype.interfaces.IContentTypeInterface)

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
                'retrieving_mime_types.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker),
        doctest.DocFileSuite(
                'event.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                globs={'print_function': print_function},
                checker=checker),
        doctest.DocFileSuite(
                'source.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker),
        doctest.DocFileSuite(
                'constraints.txt',
                checker=checker),
        doctest.DocFileSuite(
                'contentinfo.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker),
        doctest.DocFileSuite(
                'typegetter.txt',
                checker=checker),
        doctest.DocFileSuite(
                'utils.txt',
                checker=checker),
        doctest.DocFileSuite(
                'widget.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker),
        doctest.DocFileSuite(
                'codec.txt',
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                checker=checker,
        ),
        doctest.DocFileSuite(
                'configure.txt',
                setUp=testing.setUp, tearDown=testing.tearDown,
                checker=checker
        ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
