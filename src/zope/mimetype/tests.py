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

$Id$
"""
import unittest
import doctest

from zope.component import testing
import zope.interface
import zope.mimetype.interfaces


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
        doctest.DocFileSuite('retrieving_mime_types.txt',
                             setUp=testing.setUp,
                             tearDown=testing.tearDown),
        doctest.DocFileSuite('event.txt',
                             setUp=testing.setUp,
                             tearDown=testing.tearDown),
        doctest.DocFileSuite('source.txt',
                             setUp=testing.setUp,
                             tearDown=testing.tearDown),
        doctest.DocFileSuite('constraints.txt'),
        doctest.DocFileSuite('contentinfo.txt',
                             setUp=testing.setUp,
                             tearDown=testing.tearDown),
        doctest.DocFileSuite('typegetter.txt'),
        doctest.DocFileSuite('utils.txt'),
        doctest.DocFileSuite('widget.txt',
                             setUp=testing.setUp,
                             tearDown=testing.tearDown),
        doctest.DocFileSuite(
            'codec.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
