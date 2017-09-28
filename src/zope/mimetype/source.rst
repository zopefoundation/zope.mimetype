Source for MIME type interfaces
===============================

Some sample interfaces have been created in the zope.mimetype.tests
module for use in this test.  Let's import them::

  >>> from zope.mimetype.tests import (
  ...     ISampleContentTypeOne, ISampleContentTypeTwo)

The source should only include `IContentTypeInterface` interfaces that
have been registered.  Let's register one of these two interfaces so
we can test this::

  >>> import zope.component
  >>> from zope.mimetype.interfaces import IContentTypeInterface

  >>> zope.component.provideUtility(
  ...     ISampleContentTypeOne, IContentTypeInterface, name="type/one")

  >>> zope.component.provideUtility(
  ...     ISampleContentTypeOne, IContentTypeInterface, name="type/two")

We should see that these interfaces are included in the source::

  >>> from zope.mimetype import source

  >>> s = source.ContentTypeSource()

  >>> ISampleContentTypeOne in s
  True
  >>> ISampleContentTypeTwo in s
  False

Interfaces that do not implement the `IContentTypeInterface` are not
included in the source::

  >>> import zope.interface
  >>> class ISomethingElse(zope.interface.Interface):
  ...    """This isn't a content type interface."""

  >>> ISomethingElse in s
  False

The source is iterable, so we can get a list of the values::

  >>> values = list(s)

  >>> len(values)
  1
  >>> values[0] is ISampleContentTypeOne
  True

We can get terms for the allowed values::

  >>> terms = source.ContentTypeTerms(s, None)
  >>> t = terms.getTerm(ISampleContentTypeOne)
  >>> terms.getValue(t.token) is ISampleContentTypeOne
  True

Interfaces that are not in the source cause an error when a term is
requested::

  >>> terms.getTerm(ISomethingElse)
  Traceback (most recent call last):
  ...
  LookupError: value is not an element in the source

The term provides a token based on the module name of the interface::

  >>> t.token
  'zope.mimetype.tests.ISampleContentTypeOne'

The term also provides the title based on the "title" tagged value
from the interface::

  >>> t.title
  u'Type One'

Each interface provides a list of MIME types with which the interface
is associated.  The term object provides access to this list::

  >>> t.mimeTypes
  ['type/one', 'type/foo']

A list of common extensions for files of this type is also available,
though it may be empty::

  >>> t.extensions
  []

The term's value, of course, is the interface passed in::

  >>> t.value is ISampleContentTypeOne
  True

This extended term API is defined by the `IContentTypeTerm`
interface::

  >>> from zope.mimetype.interfaces import IContentTypeTerm
  >>> IContentTypeTerm.providedBy(t)
  True

The value can also be retrieved using the `getValue()` method::

  >>> iface = terms.getValue('zope.mimetype.tests.ISampleContentTypeOne')
  >>> iface is ISampleContentTypeOne
  True

Attempting to retrieve an interface that isn't in the source using the
terms object generates a LookupError::

  >>> terms.getValue('zope.mimetype.tests.ISampleContentTypeTwo')
  Traceback (most recent call last):
  ...
  LookupError: token does not represent an element in the source

Attempting to look up a junk token also generates an error::

  >>> terms.getValue('just.some.dotted.name.that.does.not.exist')
  Traceback (most recent call last):
  ...
  LookupError: could not import module for token
