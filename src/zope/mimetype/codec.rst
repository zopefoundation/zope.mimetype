Codec handling
==============

We can create codecs programatically. Codecs are registered as
utilities for ICodec with the name of their python codec.

   >>> from zope import component
   >>> from zope.mimetype.interfaces import ICodec
   >>> from zope.mimetype.codec import addCodec
   >>> sorted(component.getUtilitiesFor(ICodec))
   []
   >>> addCodec('iso8859-1', 'Western (ISO-8859-1)')
   >>> codec = component.getUtility(ICodec, name='iso8859-1')
   >>> codec
   <zope.mimetype.codec.Codec ...>
   >>> codec.name
   'iso8859-1'
   >>> addCodec('utf-8', 'Unicode (UTF-8)')
   >>> codec2 = component.getUtility(ICodec, name='utf-8')

We can programmatically add charsets to a given codec. This registers
each charset as a named utility for ICharset. It also registers the codec
as a utility for ICharsetCodec with the name of the charset.

   >>> from zope.mimetype.codec import addCharset
   >>> from zope.mimetype.interfaces import ICharset, ICharsetCodec
   >>> sorted(component.getUtilitiesFor(ICharset))
   []
   >>> sorted(component.getUtilitiesFor(ICharsetCodec))
   []
   >>> addCharset(codec.name, 'latin1')
   >>> charset = component.getUtility(ICharset, name='latin1')
   >>> charset
   <zope.mimetype.codec.Charset ...>
   >>> charset.name
   'latin1'
   >>> component.getUtility(ICharsetCodec, name='latin1') is codec
   True

When adding a charset we can state that we want that charset to be the
preferred charset for its codec.

   >>> addCharset(codec.name, 'iso8859-1', preferred=True)
   >>> addCharset(codec2.name, 'utf-8', preferred=True)

A codec can have at most one preferred charset.

   >>> addCharset(codec.name, 'test', preferred=True)
   Traceback (most recent call last):
   ...
   ValueError: Codec already has a preferred charset.

Preferred charsets are registered as utilities for
ICodecPreferredCharset under the name of the python codec.

   >>> from zope.mimetype.interfaces import ICodecPreferredCharset
   >>> preferred = component.getUtility(ICodecPreferredCharset, name='iso8859-1')
   >>> preferred
   <zope.mimetype.codec.Charset ...>
   >>> preferred.name
   'iso8859-1'
   >>> sorted(component.getUtilitiesFor(ICodecPreferredCharset))
   [(u'iso8859-1', <zope.mimetype.codec.Charset ...>),
    (u'utf-8', <zope.mimetype.codec.Charset ...>)]

We can look up a codec by the name of its charset:

   >>> component.getUtility(ICharsetCodec, name='latin1') is codec
   True
   >>> component.getUtility(ICharsetCodec, name='utf-8') is codec2
   True

Or we can look up all codecs:

   >>> sorted(component.getUtilitiesFor(ICharsetCodec))
   [(u'iso8859-1', <zope.mimetype.codec.Codec ...>),
    (u'latin1', <zope.mimetype.codec.Codec ...>),
    (u'test', <zope.mimetype.codec.Codec ...>),
    (u'utf-8', <zope.mimetype.codec.Codec ...>)]

