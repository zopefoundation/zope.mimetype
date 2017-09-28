Constraint Functions for Interfaces
===================================

The `zope.mimetype.interfaces` module defines interfaces that use some
helper functions to define constraints on the accepted data.  These
helpers are used to determine whether values conform to the what's
allowed for parts of a MIME type specification and other parts of a
Content-Type header as specified in RFC 2045.

Single Token
------------

The first is the simplest:  the `tokenConstraint()` function returns
`True` if the ASCII string it is passed conforms to the `token`
production in section 5.1 of the RFC.  Let's import the function::

  >>> from zope.mimetype.interfaces import tokenConstraint

Typical token are the major and minor parts of the MIME type and the
parameter names for the Content-Type header.  The function should
return `True` for these values::

  >>> tokenConstraint("text")
  True
  >>> tokenConstraint("plain")
  True
  >>> tokenConstraint("charset")
  True

The function should also return `True` for unusual but otherwise
normal token that may be used in some situations::

  >>> tokenConstraint("not-your-fathers-token")
  True

It must also allow extension tokens and vendor-specific tokens::

  >>> tokenConstraint("x-magic")
  True

  >>> tokenConstraint("vnd.zope.special-data")
  True

Since we expect input handlers to normalize values to lower case,
upper case text is not allowed::

  >>> tokenConstraint("Text")
  False

Non-ASCII text is also not allowed::

  >>> tokenConstraint("\x80")
  False
  >>> tokenConstraint("\xC8")
  False
  >>> tokenConstraint("\xFF")
  False

Note that lots of characters are allowed in tokens, and there are no
constraints that the token "look like" something a person would want
to read::

  >>> tokenConstraint(".-.-.-.")
  True

Other characters are disallowed, however, including all forms of
whitespace::

  >>> tokenConstraint("foo bar")
  False
  >>> tokenConstraint("foo\tbar")
  False
  >>> tokenConstraint("foo\nbar")
  False
  >>> tokenConstraint("foo\rbar")
  False
  >>> tokenConstraint("foo\x7Fbar")
  False

Whitespace before or after the token is not accepted either::

  >>> tokenConstraint(" text")
  False
  >>> tokenConstraint("plain ")
  False

Other disallowed characters are defined in the `tspecials` production
from the RFC (also in section 5.1)::

  >>> tokenConstraint("(")
  False
  >>> tokenConstraint(")")
  False
  >>> tokenConstraint("<")
  False
  >>> tokenConstraint(">")
  False
  >>> tokenConstraint("@")
  False
  >>> tokenConstraint(",")
  False
  >>> tokenConstraint(";")
  False
  >>> tokenConstraint(":")
  False
  >>> tokenConstraint("\\")
  False
  >>> tokenConstraint('"')
  False
  >>> tokenConstraint("/")
  False
  >>> tokenConstraint("[")
  False
  >>> tokenConstraint("]")
  False
  >>> tokenConstraint("?")
  False
  >>> tokenConstraint("=")
  False

A token must contain at least one character, so `tokenConstraint()`
returns false for an empty string::

  >>> tokenConstraint("")
  False


MIME Type
---------

A MIME type is specified using two tokens separated by a slash;
whitespace between the tokens and the slash must be normalized away in
the input handler.

The `mimeTypeConstraint()` function is available to test a normalized
MIME type value; let's import that function now::

  >>> from zope.mimetype.interfaces import mimeTypeConstraint

Let's test some common MIME types to make sure the function isn't
obviously insane::

  >>> mimeTypeConstraint("text/plain")
  True
  >>> mimeTypeConstraint("application/xml")
  True
  >>> mimeTypeConstraint("image/svg+xml")
  True

If parts of the MIME type are missing, it isn't accepted::

  >>> mimeTypeConstraint("text")
  False
  >>> mimeTypeConstraint("text/")
  False
  >>> mimeTypeConstraint("/plain")
  False

As for individual tokens, whitespace is not allowed::

  >>> mimeTypeConstraint("foo bar/plain")
  False
  >>> mimeTypeConstraint("text/foo bar")
  False

Whitespace is not accepted around the slash either::

  >>> mimeTypeConstraint("text /plain")
  False
  >>> mimeTypeConstraint("text/ plain")
  False

Surrounding whitespace is also not accepted::

  >>> mimeTypeConstraint(" text/plain")
  False
  >>> mimeTypeConstraint("text/plain ")
  False
