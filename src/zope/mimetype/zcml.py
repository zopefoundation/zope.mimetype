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

import os.path

from zope import interface
from zope import schema
from zope.configuration import fields

from zope.mimetype.i18n import _
from zope.mimetype import codec
from zope.mimetype import interfaces
from zope.mimetype import mtypes

try:
    from zope.browserresource.metaconfigure import icon
except ImportError: # pragma: no cover (coverage runs with the extra installed)
    def icon(*args):
        import warnings
        warnings.warn("No icon support: zope.browserresource is not installed")

import zope.component.zcml
import zope.component.interface


class IMimeTypesDirective(interface.Interface):
    """Request loading of a MIME type definition table.

    Example::

      <zope:mimeTypes file='types.csv' module="zope.mimetype.interfaces" />

    """

    file = fields.Path(
        title=_("File"),
        description=_("Path of the CSV file to load registrations from."),
        required=True,
        )

    module = fields.GlobalObject(
        title=_("Module"),
        description=_("Module which contains the interfaces"
                      " referenced from the CSV file."),
        required=True,
        )


def mimeTypesDirective(_context, file, module):
    codec.initialize(_context)
    directory = os.path.dirname(file)
    data = mtypes.read(file)
    provides = interfaces.IContentTypeInterface
    for name, info in data.items():
        iface = getattr(module, name, None)
        if iface is None:
            # create missing interface
            iface = mtypes.makeInterface(
                name, info, getattr(module, "__name__", None))
            setattr(module, name, iface)
        # Register the interface as a utility:
        _context.action(
            discriminator = None,
            callable = zope.component.interface.provideInterface,
            args = (iface.__module__ + '.' + iface.getName(), iface)
            )
        for mime_type in info[2]:
            # Register the interface as the IContentTypeInterface
            # utility for each appropriate MIME type:
            _context.action(
                discriminator = ('utility', provides, mime_type),
                callable = zope.component.zcml.handler,
                args = ('registerUtility', iface, provides, mime_type),
                )
        icon_path = os.path.join(directory, info[3])
        if icon_path and os.path.isfile(icon_path):
            icon(_context, "zmi_icon", iface, icon_path)


class ICodecDirective(interface.Interface):
    """Defines a codec.

    Example::

       <zope:codec name="iso8859-1" title="Western (ISO-8859-1)">
          ...
       </zope:codec>
    """

    name = schema.ASCIILine(
        title=_('Name'),
        description=_('The name of the Python codec.'),
        required=True,
        )

    title = fields.MessageID(
        title=_('Title'),
        description=_('The human-readable name for this codec.'),
        required=False,
        )

class ICharsetDirective(interface.Interface):
    """Defines a charset in a codec.

    Example::

       <charset name="iso8859-1" preferred="True" />
       <charset name="latin1" />

    """

    name = schema.ASCIILine(
        title=_('Name'),
        description=_('The name of the Python codec.'),
        required=True,
        )

    preferred = schema.Bool(
        title=_('Preferred'),
        description=_('Is this is the preferred charset for the encoding.'),
        required=False,
        )


class CodecDirective(object):
    def __init__(self, _context, name, title):
        self.name = name
        self.title = title
        _context.action(
            discriminator = None,
            callable = codec.addCodec,
            args = (name, title),
            )

    def charset(self, _context, name, preferred=False):
        _context.action(
            discriminator = (self.name, name),
            callable = codec.addCharset,
            args = (self.name, name, preferred),
            )
