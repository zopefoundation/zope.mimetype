Events and content-type changes
===============================

The `IContentTypeChangedEvent` is fired whenever an object's
`IContentTypeInterface` is changed.  This includes the cases when a
content type interface is applied to an object that doesn't have one,
and when the content type interface is removed from an object.

Let's start the demonstration by defining a subscriber for the event
that simply prints out the information from the event object::

  >>> def handler(event):
  ...     print("changed content type interface:")
  ...     print("  from:", event.oldContentType)
  ...     print("    to:", event.newContentType)

We'll also define a simple content object::

  >>> import zope.interface

  >>> class IContent(zope.interface.Interface):
  ...     pass

  >>> @zope.interface.implementer(IContent)
  ... class Content(object):
  ...     def __str__(self):
  ...         return "<MyContent>"

  >>> obj = Content()

We'll also need a couple of content type interfaces::

  >>> from zope.mimetype import interfaces

  >>> class ITextPlain(interfaces.IContentTypeEncoded):
  ...     """text/plain"""
  >>> ITextPlain.setTaggedValue("mimeTypes", ["text/plain"])
  >>> ITextPlain.setTaggedValue("extensions", [".txt"])
  >>> zope.interface.directlyProvides(
  ...     ITextPlain, interfaces.IContentTypeInterface)

  >>> class IOctetStream(interfaces.IContentType):
  ...     """application/octet-stream"""
  >>> IOctetStream.setTaggedValue("mimeTypes", ["application/octet-stream"])
  >>> IOctetStream.setTaggedValue("extensions", [".bin"])
  >>> zope.interface.directlyProvides(
  ...     IOctetStream, interfaces.IContentTypeInterface)

Let's register our subscriber::

  >>> import zope.component
  >>> import zope.component.interfaces
  >>> zope.component.provideHandler(
  ...     handler,
  ...     (zope.component.interfaces.IObjectEvent,))

Changing the content type interface on an object is handled by the
`zope.mimetype.event.changeContentType()` function.  Let's import that
module and demonstrate that the expected event is fired
appropriately::

  >>> from zope.mimetype import event

Since the object currently has no content type interface, "removing"
the interface does not affect the object and the event is not fired::

  >>> event.changeContentType(obj, None)

Setting a content type interface on an object that doesn't have one
will cause the event to be fired, with the `.oldContentType` attribute
on the event set to `None`::

  >>> event.changeContentType(obj, ITextPlain)
  changed content type interface:
    from: None
      to: <InterfaceClass __builtin__.ITextPlain>

Calling the `changeContentType()` function again with the same "new"
content type interface causes no change, so the event is not fired
again::

  >>> event.changeContentType(obj, ITextPlain)

Providing a new interface does cause the event to be fired again::

  >>> event.changeContentType(obj, IOctetStream)
  changed content type interface:
    from: <InterfaceClass __builtin__.ITextPlain>
      to: <InterfaceClass __builtin__.IOctetStream>

Similarly, removing the content type interface triggers the event as
well::

  >>> event.changeContentType(obj, None)
  changed content type interface:
    from: <InterfaceClass __builtin__.IOctetStream>
      to: None
