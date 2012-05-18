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
"""Implementation of and support for the `IContentTypeChangedEvent`.

"""
__docformat__ = "reStructuredText"

import zope.event
import zope.component.interfaces
import zope.interface
import zope.mimetype.interfaces
import zope.security.proxy


@zope.interface.implementer(zope.mimetype.interfaces.IContentTypeChangedEvent)
class ContentTypeChangedEvent(zope.component.interfaces.ObjectEvent):

    def __init__(self, object, oldContentType, newContentType):
        super(ContentTypeChangedEvent, self).__init__(object)
        self.newContentType = newContentType
        self.oldContentType = oldContentType


def changeContentType(object, newContentType):
    """Set the content type interface for the object.

    If this represents a change, an `IContentTypeChangedEvent` will be
    fired.

    """
    ifaces = zope.interface.directlyProvidedBy(object)
    oldContentType = None
    for iface in ifaces:
        if zope.mimetype.interfaces.IContentTypeInterface.providedBy(iface):
            oldContentType = iface
            ifaces -= iface
            break
    if newContentType is not oldContentType:
        # update the interfaces for the object:
        if newContentType is not None:
            ifaces += newContentType
        zope.interface.directlyProvides(object, *ifaces)
        # fire the event:
        event = ContentTypeChangedEvent(
            zope.security.proxy.ProxyFactory(object),
            oldContentType,
            newContentType)
        zope.event.notify(event)
