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

# There's a zope.contenttype module that exports a similar API,
# but that's pretty hueristic.  Some of this should perhaps be folded
# back into that, or this package could provide a replacement.
#
import mimetypes
import codecs

from zope import interface
from zope.mimetype import interfaces
import zope.contenttype.parse


def mimeTypeGetter(name=None, data=None, content_type=None):
    """A minimal extractor that never attempts to guess."""
    if name is None and data is None and content_type is None:
        return None
    if content_type:
        try:
            major, minor, _params = zope.contenttype.parse.parseOrdered(
                content_type)
        except ValueError:
            pass
        else:
            return "%s/%s" % (major, minor)

    return None

interface.directlyProvides(mimeTypeGetter, interfaces.IMimeTypeGetter)


def mimeTypeGuesser(name=None, data=None, content_type=None):
    """An extractor that tries to guess the content type based on the
    name and data if the input contains no content type information.
    """
    if name is None and data is None and content_type is None:
        return None

    mimeType = mimeTypeGetter(name=name, data=data, content_type=content_type)

    if name and not mimeType:
        mimeType, _encoding = mimetypes.guess_type(name, strict=True)
        if not mimeType:
            mimeType, _encoding = mimetypes.guess_type(name, strict=False)
        #
        # XXX If `encoding` is not None, we should re-consider the
        # guess, since the encoding here is Content-Encoding, not
        # charset.  In particular, things like .tar.gz map to
        # ('application/x-tar', 'gzip'), which may require different
        # handling, or at least a separate content-type.

    if data and not mimeType:
        # no idea, really, but let's sniff a few common things:
        for prefix, sniffed_type, _charset in _prefix_table:
            if data.startswith(prefix):
                mimeType = sniffed_type
                break

    return mimeType

interface.directlyProvides(mimeTypeGuesser, interfaces.IMimeTypeGetter)


def smartMimeTypeGuesser(name=None, data=None, content_type=None):
    """An extractor that checks the content for a variety of
    constructs to try and refine the results of the
    `mimeTypeGuesser()`. This is able to do things like check for
    XHTML that's labelled as HTML in upload data.
    """
    mimeType = mimeTypeGuesser(name=name, data=data, content_type=content_type)

    if data and mimeType == "text/html":
        for prefix, _mimetype, _charset in _xml_prefix_table:
            if data.startswith(prefix):
                # don't use text/xml from the table, but take
                # advantage of the text/html hint (from the upload
                # or mimetypes.guess_type())
                mimeType = "application/xhtml+xml"
                break

    return mimeType

interface.directlyProvides(smartMimeTypeGuesser, interfaces.IMimeTypeGetter)


# Very simple magic numbers table for a few things we want to be good
# at identifying even if we get no help from the input:
#
_xml_prefix_table = (
    # prefix, mimeType, charset
    (b"<?xml",                   "text/xml",     None),
    (b"\xef\xbb\xbf<?xml",       "text/xml",     "utf-8"),    # w/ BOM
    (b"\0<\0?\0x\0m\0l",         "text/xml",     "utf-16be"),
    (b"<\0?\0x\0m\0l\0",         "text/xml",     "utf-16le"),
    (b"\xfe\xff\0<\0?\0x\0m\0l", "text/xml",     "utf-16be"), # w/ BOM
    (b"\xff\xfe<\0?\0x\0m\0l\0", "text/xml",     "utf-16le"), # w/ BOM
    )
_prefix_table = _xml_prefix_table + (
    (b"<html",                   "text/html",    None),
    (b"<HTML",                   "text/html",    None),
    (b"GIF89a",                  "image/gif",    None),
    # PNG Signature: bytes 137 80 78 71 13 10 26 10
    (b"\x89PNG\r\n\x1a\n",       "image/png",    None),
    )


def charsetGetter(name=None, data=None, content_type=None):
    """Default implementation of `zope.mimetype.interfaces.ICharsetGetter`."""
    if name is None and data is None and content_type is None:
        return None
    if content_type:
        try:
            major, minor, params = zope.contenttype.parse.parse(content_type)
        except ValueError:
            pass
        else:
            if params.get("charset"):
                return params["charset"].lower()
    if data:
        if data.startswith(codecs.BOM_UTF16_LE):
            return 'utf-16le'
        elif data.startswith(codecs.BOM_UTF16_BE):
            return 'utf-16be'
        try:
            data.decode('ascii')
            return 'ascii'
        except UnicodeDecodeError:
            try:
                data.decode('utf-8')
                return 'utf-8'
            except UnicodeDecodeError:
                pass
    return None

interface.directlyProvides(charsetGetter, interfaces.ICharsetGetter)
