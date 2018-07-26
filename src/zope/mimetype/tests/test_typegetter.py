##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import

import unittest

from zope.mimetype import typegetter


class TestMimeTypeGuesser(unittest.TestCase):

    def test_bytes_data_and_no_mime_type_or_name(self):
        # Python 3: bytes data and no content type but something that
        # looked like html used to cause a TypeError
        # Similar to https://github.com/zopefoundation/zope.mimetype/issues/6

        mimeType = typegetter.mimeTypeGuesser(data=b'<html')
        self.assertEqual('text/html', mimeType)

        mimeType = typegetter.mimeTypeGuesser(data=b'<HTML')
        self.assertEqual('text/html', mimeType)


        mimeType = typegetter.mimeTypeGuesser(data=b'GIF89a')
        self.assertEqual('image/gif', mimeType)

        mimeType = typegetter.mimeTypeGuesser(data=b"\x89PNG\r\n\x1a\n")
        self.assertEqual('image/png', mimeType)

    def test_name_provided_unguessable(self):
        mimeType = typegetter.mimeTypeGuesser(name="something")
        self.assertIsNone(mimeType)


class TestSmartMimeTypeGuesser(unittest.TestCase):

    def test_bytes_and_text_html_type_error(self):
        # Python 3: bytes data and text/html content type
        # used to cause a TypeError
        # https://github.com/zopefoundation/zope.mimetype/issues/6

        mimeType = typegetter.smartMimeTypeGuesser(data=b'I am bytes',
                                                   content_type='text/html')
        self.assertEqual('text/html', mimeType)


class TestCharsetGetter(unittest.TestCase):

    def test_parse_bad_content_type(self):
        charset = typegetter.charsetGetter(content_type="not a content type")
        self.assertIsNone(charset)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
