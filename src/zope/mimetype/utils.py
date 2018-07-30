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
"""Utility helpers
"""
try:
    from email.charset import Charset
except ImportError: # pragma: no cover
    # Py2: Old name. (Note, on case-insensitive filesystems,
    # we can import with either. This complicates coverage.)
    from email.Charset import Charset


def decode(s, charset_name):
    "given a string and a IANA character set name, decode string to unicode"
    codec = Charset(charset_name).input_codec
    if codec is None:
        return s.decode()
    else:
        return s.decode(codec)
