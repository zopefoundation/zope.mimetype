Retrieving Content Type Information
===================================

MIME Types
----------

We'll start by initializing the interfaces and registrations for the
content type interfaces.  This is normally done via ZCML.

    >>> from zope.mimetype import mtypes
    >>> mtypes.setup()

A utility is used to retrieve MIME types.

    >>> from zope import component
    >>> from zope.mimetype import typegetter
    >>> from zope.mimetype.interfaces import IMimeTypeGetter
    >>> component.provideUtility(typegetter.smartMimeTypeGuesser,
    ...                          provides=IMimeTypeGetter)
    >>> mime_getter = component.getUtility(IMimeTypeGetter)

To map a particular file name, file contents, and content type to a MIME type.

    >>> mime_getter(name='file.txt', data='A text file.',
    ...             content_type='text/plain')
    'text/plain'

In the default implementation if not enough information is given to discern a
MIME type, None is returned.

    >>> mime_getter() is None
    True

Character Sets
--------------

A utility is also used to retrieve character sets (charsets).

    >>> from zope.mimetype.interfaces import ICharsetGetter
    >>> component.provideUtility(typegetter.charsetGetter,
    ...                          provides=ICharsetGetter)
    >>> charset_getter = component.getUtility(ICharsetGetter)

To map a particular file name, file contents, and content type to a charset.

    >>> charset_getter(name='file.txt', data='This is a text file.',
    ...                content_type='text/plain;charset=ascii')
    'ascii'

In the default implementation if not enough information is given to discern a
charset, None is returned.

    >>> charset_getter() is None
    True

Finding Interfaces
------------------

Given a MIME type we need to be able to find the appropriate interface.

    >>> from zope.mimetype.interfaces import IContentTypeInterface
    >>> component.getUtility(IContentTypeInterface, name=u'text/plain')
    <InterfaceClass zope.mimetype.mtypes.IContentTypeTextPlain>

It is also possible to enumerate all content type interfaces.

    >>> utilities = list(component.getUtilitiesFor(IContentTypeInterface))

If you want to find an interface from a MIME string, you can use the
utilityies.

    >>> component.getUtility(IContentTypeInterface, name='text/plain')
    <InterfaceClass zope.mimetype.mtypes.IContentTypeTextPlain>
