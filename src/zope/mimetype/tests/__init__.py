##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
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
