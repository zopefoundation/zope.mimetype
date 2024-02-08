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
# -*- coding: utf-8 -*-
"""
Tests for contentinfo.py

"""

import unittest

from zope.testing import cleanup

from zope import interface
from zope.mimetype.contentinfo import ContentInfo


class TestContentinfo(cleanup.CleanUp,
                      unittest.TestCase):

    def test_codec_cant_decode_all(self):
        from zope.mimetype.interfaces import IContentTypeAware

        @interface.implementer(IContentTypeAware)
        class Content:
            mimeType = 'text/plain'
            parameters = ()

        class Codec:
            def decode(self, s):
                return '', 0

        info = ContentInfo(Content())
        # ContentInfo caches the codec, take advantage of that.
        info._codec = Codec()

        with self.assertRaisesRegex(ValueError, "not completely consumed"):
            info.decode('foo')
