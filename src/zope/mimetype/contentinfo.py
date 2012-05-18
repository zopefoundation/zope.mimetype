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
"""Default IContentInfo implementation.

"""
__docformat__ = "reStructuredText"

import zope.component
import zope.contenttype.parse
import zope.interface
import zope.mimetype.interfaces


@zope.interface.implementer(zope.mimetype.interfaces.IContentInfo)
@zope.component.adapter(zope.interface.Interface)
class ContentInfo(object):
    """Basic IContentInfo that provides information from an IContentTypeAware.
    """
    def __init__(self, context):
        self.context = context
        aware = zope.mimetype.interfaces.IContentTypeAware(context)
        self.effectiveMimeType = aware.mimeType
        self.effectiveParameters = dict(aware.parameters)
        if self.effectiveParameters:
            encoded = zope.mimetype.interfaces.IContentTypeEncoded.providedBy(
                context)
            if "charset" in self.effectiveParameters and not encoded:
                del self.effectiveParameters["charset"]
            major, minor = self.effectiveMimeType.split("/")
            self.contentType = zope.contenttype.parse.join(
                (major, minor, self.effectiveParameters))
        else:
            self.contentType = self.effectiveMimeType

    def getCodec(self):
        if "_codec" in self.__dict__:
            return self._codec
        isencoded = zope.mimetype.interfaces.IContentTypeEncoded.providedBy(
            self.context)
        if isencoded:
            charset = self.effectiveParameters.get("charset")
            if charset:
                utility = zope.component.queryUtility(
                    zope.mimetype.interfaces.ICharset, charset)
                if utility is None:
                    raise ValueError("unsupported charset: %r" % charset)
                codec = zope.component.getUtility(
                    zope.mimetype.interfaces.ICodec, utility.encoding)
                self._codec = codec
            else:
                raise ValueError("charset not known")
        else:
            self._codec = None
        return self._codec

    def decode(self, s):
        codec = self.getCodec()
        if codec is not None:
            text, consumed = codec.decode(s)
            if consumed != len(s):
                raise ValueError("data not completely consumed")
            return text
        else:
            raise ValueError("no matching codec found")
