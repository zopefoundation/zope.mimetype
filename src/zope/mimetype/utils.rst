The utils module contains various helpers for working with data goverened
by MIME content type information, as found in the HTTP Content-Type header:
mime types and character sets.

The decode function takes a string and an IANA character set name and
returns a unicode object decoded from the string, using the codec associated
with the character set name.  Errors will generally arise from the unicode
conversion rather than the mapping of character set to codec, and will be
LookupErrors (the character set did not cleanly convert to a codec that
Python knows about) or UnicodeDecodeErrors (the string included characters
that were not in the range of the codec associated with the character set).

    >>> original = b'This is an o with a slash through it: \xb8.'
    >>> charset = 'Latin-7' # Baltic Rim or iso-8859-13
    >>> from zope.mimetype import utils
    >>> utils.decode(original, charset)
    u'This is an o with a slash through it: \xf8.'
    >>> utils.decode(original, 'foo bar baz')
    Traceback (most recent call last):
    ...
    LookupError: unknown encoding: foo bar baz
    >>> utils.decode(original, 'iso-ir-6') # alias for ASCII
    ... # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    UnicodeDecodeError: 'ascii' codec can't decode...
