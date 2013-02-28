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
"""Mime-Types management
"""
import os
import csv
import zope.interface
from zope.component import provideUtility
from zope.interface.interface import InterfaceClass
from zope.mimetype.interfaces import IContentType, IContentTypeEncoded
from zope.mimetype.interfaces import IContentTypeInterface
from zope.mimetype.i18n import _

def read(file_name):
    file = open(file_name)
    result = {}
    for name, title, extensions, mime_types, icon_name, encoded in csv.reader(file):
        extensions = extensions.split()
        mime_types = mime_types.split()
        encoded = (encoded.strip().lower() == 'yes')
        result[name] = (title.strip(), extensions, mime_types,
                        icon_name.strip(), encoded)
    file.close()
    return result

def getInterfaces(data, module=None):
    results = {}
    if module is None:
        module = __name__
    globs = globals()
    for name, info in data.items():
        interface = globs.get(name)
        if interface is None:
            interface = makeInterface(name, info, module)
            globs[name] = interface
        results[name] = interface
    return results

def makeInterface(name, info, module):
    title, extensions, mime_types, icon_name, encoded = info
    if encoded:
        base = IContentTypeEncoded
    else:
        base = IContentType
    interface = InterfaceClass(name, bases=(base,),  __module__=module)
    zope.interface.directlyProvides(interface, IContentTypeInterface)
    interface.setTaggedValue('extensions', extensions)
    interface.setTaggedValue('mimeTypes', mime_types)
    interface.setTaggedValue('title', _(title, default=title))
    return interface


def registerUtilities(interfaces, data):
    for name, interface in interfaces.items():
        for mime_type in data[name][2]:
            provideUtility(interface, provides=IContentTypeInterface,
                           name=mime_type)


here = os.path.dirname(os.path.abspath(__file__))
types_data = os.path.join(here, "types.csv")

def setup():
    data = read(types_data)
    interfaces = getInterfaces(data)
    registerUtilities(interfaces, data)
