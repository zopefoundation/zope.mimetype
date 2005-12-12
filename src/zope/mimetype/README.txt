============================
The Zope MIME Infrastructure
============================

This package provides a way to work with MIME content types.  There
are several interfaces defined here, many of which are used primarily
to look things up based on different bits of information.

The basic idea behind this is that content objects should provide an
interface based on the actual content type they implement.  For
example, objects that represent text/xml or application/xml documents
should be marked mark with the `IContentTypeXml` interface.  This can
allow additional views to be registered based on the content type, or
subscribers may be registered to perform other actions based on the
content type.

One aspect of the content type that's important for all documents is
that the content type interface determines whether the object data is
interpreted as an encoded text document.  Encoded text documents, in
particular, can be decoded to obtain a single Unicode string.  The
content type intefaces for encoded text must derive from
`IContentTypeEncoded`.  (All content type interfaces derive from
`IContentType` and directly provide `IContentTypeInterface`.)

The default configuration provides direct support for a variety of
common document types found in office environments.

Supported lookups
-----------------

Several different queries are supported by this package:

- Given a MIME type expressed as a string, the associated interface,
  if any, can be retrieved using::

    # `mimeType` is the MIME type as a string
    interface = queryUtility(IContentTypeInterface, mimeType)

- Given a charset name, the associated `ICodec` instance can be
  retrieved using::

    # `charsetName` is the charset name as a string
    codec = queryUtility(ICharsetCodec, charsetName)

- Given a codec, the preferred charset name can be retrieved using::

    # `codec` is an `ICodec` instance:
    charsetName = getUtility(ICodecPreferredCharset, codec.name).name

- Given any combination of a suggested file name, file data, and
  content type header, a guess at a reasonable MIME type can be made
  using::

    # `filename` is a suggested file name, or None
    # `data` is uploaded data, or None
    # `content_type` is a Content-Type header value, or None
    #
    mimeType = getUtility(IMimeTypeGetter)(
        name=filename, data=data, content_type=content_type)

- Given any combination of a suggested file name, file data, and
  content type header, a guess at a reasonable charset name can be
  made using::

    # `filename` is a suggested file name, or None
    # `data` is uploaded data, or None
    # `content_type` is a Content-Type header value, or None
    #
    charsetName = getUtility(ICharsetGetter)(
        name=filename, data=data, content_type=content_type)
