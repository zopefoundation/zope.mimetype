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
"""interfaces for mimetype package
"""
import re

import zope.component.interfaces
import zope.schema.interfaces

from zope import interface, schema
from zope.configuration.fields import MessageID
from zope.mimetype.i18n import _


# Note that MIME types and content type parameter names are considered
# case-insensitive.  For our purposes, they should always be
# lower-cased on input.  This should be handled by the input machinery
# (widgets) rather than in the application or MIME-handling code.
# Constraints defined here specify lower case values.
#
# The MIME type is defined to be two tokens separated by a slash; for
# our purposes, any whitespace between the tokens must be normalized
# by removing it.  This too should be handled by input mechanisms.

# This RE really assumes you know the ASCII codes; note that upper
# case letters are not accepted; tokens must be normalized.
# http://czyborra.com/charsets/iso646.html
# http://www.faqs.org/rfcs/rfc2045.html
_token_re = r"[!#$%&'*+\-.\d^_`a-z{|}~]+"
_token_rx = re.compile("%s$" % _token_re)
_mime_type_rx = re.compile("%s/%s$" % (_token_re, _token_re))


# These helpers are used to define constraints for specific schema
# fields.  Documentation and tests for these are located in
# constraints.txt.

def mimeTypeConstraint(value):
    """Return `True` iff `value` is a syntactically legal MIME type."""
    return _mime_type_rx.match(value) is not None

def tokenConstraint(value):
    """Return `True` iff `value` is a syntactically legal RFC 2045 token."""
    return _token_rx.match(value) is not None


class IContentTypeAware(interface.Interface):
    """Interface for MIME content type information.

    Objects that can provide content type information about the data
    they contain, such as file objects, should be adaptable to this
    interface.

    """

    parameters = schema.Dict(
        title=_('Mime Type Parameters'),
        description=_("The MIME type parameters (such as charset)."),
        required=True,
        key_type=schema.ASCIILine(constraint=tokenConstraint)
        )

    mimeType = schema.ASCIILine(
        title=_('Mime Type'),
        description=_("The mime type explicitly specified for the object"
                      " that this MIME information describes, if any. "
                      " May be None, or an ASCII MIME type string of the"
                      " form major/minor."),
        constraint=mimeTypeConstraint,
        required=False,
        )


class IContentTypeInterface(interface.Interface):
    """Interface that describes a logical mime type.

    Interfaces that provide this interfaces are content-type
    interfaces.

    Most MIME types are described by the IANA MIME-type registry
    (http://www.iana.org/assignments/media-types/).

    """


class IContentType(interface.Interface):
    """Marker interface for objects that represent content with a MIME type.
    """
interface.directlyProvides(IContentType, IContentTypeInterface)


class IContentTypeEncoded(IContentType):
    """Marker interface for content types that care about encoding.

    This does not imply that encoding information is known for a
    specific object.

    Content types that derive from `IContentTypeEncoded` support a
    content type parameter named 'charset', and that parameter is used
    to control encoding and decoding of the text.

    For example, interfaces for text/* content types all derive from
    this base interface.

    """
interface.directlyProvides(IContentTypeEncoded, IContentTypeInterface)


class IContentTypeChangedEvent(zope.component.interfaces.IObjectEvent):
    """The content type for an object has changed.

    All changes of the `IContentTypeInterface` for an object are
    reported by this event, including the setting of an initial
    content type and the removal of the content type interface.

    This event should only be used if the content type actually
    changes.

    """

    newContentType = interface.Attribute(
        """Content type interface after the change, if any, or `None`.
        """)

    oldContentType = interface.Attribute(
        """Content type interface before the change, if any, or `None`.
        """)


class IContentTypeTerm(zope.schema.interfaces.ITitledTokenizedTerm):
    """Extended term that describes a content type interface."""

    mimeTypes = schema.List(
        title=_("MIME types"),
        description=_("List of MIME types represented by this interface;"
                      " the first should be considered the preferred"
                      " MIME type."),
        required=True,
        min_length=1,
        value_type=schema.ASCIILine(constraint=mimeTypeConstraint),
        readonly=True,
        )

    extensions = schema.List(
        title=_("Extensions"),
        description=_("Filename extensions commonly associated with this"
                      " type of file."),
        required=True,
        min_length=0,
        readonly=True,
        )

class IContentTypeSource(zope.schema.interfaces.ISource,
                         zope.schema.interfaces.IIterableSource):
    """Source for content types."""


class IContentInfo(interface.Interface): # XXX
    """Interface describing effective MIME type information.

    When using MIME data from an object, an application should adapt
    the object to this interface to determine how it should be
    interpreted.  This may be different from the information

    """

    effectiveMimeType = schema.ASCIILine(
        title=_("Effective MIME type"),
        description=_("MIME type that should be reported when"
                      " downloading the document this `IContentInfo`"
                      " object is for."),
        required=False,
        constraint=mimeTypeConstraint,
        )

    effectiveParameters = schema.Dict(
        title=_("Effective parameters"),
        description=_("Content-Type parameters that should be reported "
                      " when downloading the document this `IContentInfo`"
                      " object is for."),
        required=True,
        key_type=schema.ASCIILine(constraint=tokenConstraint),
        value_type=schema.ASCII(),
        )

    contentType = schema.ASCIILine(
        title=_("Content type"),
        description=_("The value of the Content-Type header,"
                      " including both the MIME type and any parameters."),
        required=False,
        )

    def getCodec():
        """Return an `ICodec` that should be used to decode/encode data.

        This should return `None` if the object's `IContentType` interface
        does not derive from `IContentTypeEncoded`.

        If the content type is encoded and no encoding information is
        available in the `effectiveParameters`, this method may return
        None, or may provide a codec based on application policy.

        If `effectiveParameters` indicates a specific charset, and no
        codec is registered to support that charset, `ValueError` will
        be raised.

        """

    def decode(s):
        """Return the decoding of `s` based on the effective encoding.

        The effective encoding is determined by the return from the
        `getCodec()` method.

        `ValueError` is raised if no codec can be found for the
        effective charset.

        """


class IMimeTypeGetter(interface.Interface):
    """A utility that looks up a MIME type string."""

    def __call__(name=None, data=None, content_type=None):
        """Look up a MIME type.

        If a MIME type cannot be determined based on the input,
        this returns `None`.

        :keyword bytes data: If given, the bytes data to get a MIME
            type for. This may be examined for clues about the type.
        """


class ICharsetGetter(interface.Interface):
    """A utility that looks up a character set (charset)."""

    def __call__(name=None, data=None, content_type=None):
        """Look up a charset.

        If a charset cannot be determined based on the input,
        this returns `None`.

        """


class ICodec(interface.Interface):
    """Information about a codec."""

    name = schema.ASCIILine(
        title=_('Name'),
        description=_('The name of the Python codec.'),
        required=True,
        )

    title = MessageID(
        title=_('Title'),
        description=_('The human-readable name of this codec.'),
        required=True,
        )

    def encode(input, errors='strict'):
        """Encodes the input and returns a tuple (output, length consumed).
        """

    def decode(input, errors='strict'):
        """Decodes the input and returns a tuple (output, length consumed).
        """

    def reader(stream, errors='strict'):
        """Construct a StreamReader object for this codec."""

    def writer(stream, errors='strict'):
        """Construct a StramWriter object for this codec."""


class ICharset(interface.Interface):
    """Information about a charset"""

    name = schema.ASCIILine(
        title=_('Name'),
        description=_("The charset name. This is what is used for the "
                      "'charset' parameter in content-type headers."),
        required=True,
        )

    encoding = schema.ASCIILine(
        # This *must* match the `name` of the ICodec that's used to
        # handle this charset.
        title=_('Encoding'),
        description=_("The id of the encoding used for this charset."),
        required=True,
        )


class ICodecPreferredCharset(interface.Interface):
    """Marker interface for locating the preferred charset for a Codec."""


class ICharsetCodec(interface.Interface):
    """Marker interface for locating the codec for a given charset."""

class ICodecTerm(zope.schema.interfaces.ITitledTokenizedTerm):
    """Extended term that describes a content type interface."""

    preferredCharset = schema.ASCIILine(
        title=_("Preferred Charset"),
        description=_("Charset that should be used to represent the codec"),
        required=False,
        readonly=True,
        )


class ICodecSource(zope.schema.interfaces.IIterableSource):
    """Source for codecs."""
