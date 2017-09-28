Minimal IContentInfo Implementation
===================================

The `zope.mimetype.contentinfo` module provides a minimal
`IContentInfo` implementation that adds no information to what's
provided by a content object.  This represents the most conservative
content-type policy that might be useful.

Let's take a look at how this operates by creating a couple of
concrete content-type interfaces::

  >>> from zope.mimetype import interfaces

  >>> class ITextPlain(interfaces.IContentTypeEncoded):
  ...     """text/plain"""

  >>> class IApplicationOctetStream(interfaces.IContentType):
  ...     """application/octet-stream"""

Now, we'll create a minimal content object that provide the necessary
information::

  >>> import zope.interface

  >>> @zope.interface.implementer(interfaces.IContentTypeAware)
  ... class Content(object):
  ...     def __init__(self, mimeType, charset=None):
  ...         self.mimeType = mimeType
  ...         self.parameters = {}
  ...         if charset:
  ...             self.parameters["charset"] = charset

We can now create examples of both encoded and non-encoded content::

  >>> encoded = Content("text/plain", "utf-8")
  >>> zope.interface.alsoProvides(encoded, ITextPlain)

  >>> unencoded = Content("application/octet-stream")
  >>> zope.interface.alsoProvides(unencoded, IApplicationOctetStream)

The minimal IContentInfo implementation only exposes the information
available to it from the base content object.  Let's take a look at
the unencoded content first::

  >>> from zope.mimetype import contentinfo
  >>> ci = contentinfo.ContentInfo(unencoded)
  >>> ci.effectiveMimeType
  'application/octet-stream'
  >>> ci.effectiveParameters
  {}
  >>> ci.contentType
  'application/octet-stream'

For unencoded content, there is never a codec::

  >>> print(ci.getCodec())
  None

It is also disallowed to try decoding such content::

  >>> ci.decode("foo")
  Traceback (most recent call last):
  ...
  ValueError: no matching codec found

Attemping to decode data using an uncoded object causes an exception
to be raised::

  >>> print(ci.decode("data"))
  Traceback (most recent call last):
  ...
  ValueError: no matching codec found

If we try this with encoded data, we get somewhat different behavior::

  >>> ci = contentinfo.ContentInfo(encoded)
  >>> ci.effectiveMimeType
  'text/plain'
  >>> ci.effectiveParameters
  {'charset': 'utf-8'}
  >>> ci.contentType
  'text/plain;charset=utf-8'

The `getCodec()` and `decode()` methods can be used to handle encoded
data using the encoding indicated by the ``charset`` parameter.  Let's
store some UTF-8 data in a variable::

  >>> utf8_data = b"\xAB\xBB".decode("iso-8859-1").encode("utf-8")
  >>> utf8_data
  '\xc2\xab\xc2\xbb'

We want to be able to decode the data using the `IContentInfo`
object.  Let's try getting the corresponding `ICodec` object using
`getCodec()`::

  >>> codec = ci.getCodec()
  Traceback (most recent call last):
  ...
  ValueError: unsupported charset: 'utf-8'

So, we can't proceed without some further preparation.  What we need
is to register an `ICharset` for UTF-8.  The `ICharset` will need a
reference (by name) to a `ICodec` for UTF-8.  So let's create those
objects and register them::

  >>> import codecs
  >>> from zope.mimetype.i18n import _

  >>> @zope.interface.implementer(interfaces.ICodec)
  ... class Utf8Codec(object):
  ...
  ...     name = "utf-8"
  ...     title = _("UTF-8")
  ...
  ...     def __init__(self):
  ...         ( self.encode,
  ...           self.decode,
  ...           self.reader,
  ...           self.writer
  ...           ) = codecs.lookup(self.name)

  >>> utf8_codec = Utf8Codec()

  >>> @zope.interface.implementer(interfaces.ICharset)
  ... class Utf8Charset(object):
  ...
  ...     name = utf8_codec.name
  ...     encoding = name

  >>> utf8_charset = Utf8Charset()

  >>> import zope.component

  >>> zope.component.provideUtility(
  ...     utf8_codec, interfaces.ICodec, utf8_codec.name)
  >>> zope.component.provideUtility(
  ...     utf8_charset, interfaces.ICharset, utf8_charset.name)

Now that that's been initialized, let's try getting the codec again::

  >>> codec = ci.getCodec()
  >>> codec.name
  'utf-8'

  >>> codec.decode(utf8_data)
  (u'\xab\xbb', 4)

We can now check that the `decode()` method of the `IContentInfo` will
decode the entire data, returning the Unicode representation of the
text::

  >>> ci.decode(utf8_data)
  u'\xab\xbb'

Another possibilty, of course, is that you have content that you know
is encoded text of some sort, but you don't actually know what
encoding it's in::

  >>> encoded2 = Content("text/plain")
  >>> zope.interface.alsoProvides(encoded2, ITextPlain)

  >>> ci = contentinfo.ContentInfo(encoded2)
  >>> ci.effectiveMimeType
  'text/plain'
  >>> ci.effectiveParameters
  {}
  >>> ci.contentType
  'text/plain'

  >>> ci.getCodec()
  Traceback (most recent call last):
  ...
  ValueError: charset not known

It's also possible that the initial content type information for an
object is incorrect for some reason.  If the browser provides a
content type of "text/plain; charset=utf-8", the content will be seen
as encoded.  A user correcting this content type using UI elements
can cause the content to be considered un-encoded.  At this point,
there should no longer be a charset parameter to the content type, and
the content info object should reflect this, though the previous
encoding information will be retained in case the content type should
be changed to an encoded type in the future.

Let's see how this behavior will be exhibited in this API.  We'll
start by creating some encoded content::

  >>> content = Content("text/plain", "utf-8")
  >>> zope.interface.alsoProvides(content, ITextPlain)

We can see that the encoding information is included in the effective
MIME type information provided by the content-info object::

  >>> ci = contentinfo.ContentInfo(content)
  >>> ci.effectiveMimeType
  'text/plain'
  >>> ci.effectiveParameters
  {'charset': 'utf-8'}

We now change the content type information for the object::

  >>> ifaces = zope.interface.directlyProvidedBy(content)
  >>> ifaces -= ITextPlain
  >>> ifaces += IApplicationOctetStream
  >>> zope.interface.directlyProvides(content, *ifaces)
  >>> content.mimeType = 'application/octet-stream'

At this point, a content type object would provide different
information::

  >>> ci = contentinfo.ContentInfo(content)
  >>> ci.effectiveMimeType
  'application/octet-stream'
  >>> ci.effectiveParameters
  {}

The underlying content type parameters still contain the original
encoding information, however::

  >>> content.parameters
  {'charset': 'utf-8'}
