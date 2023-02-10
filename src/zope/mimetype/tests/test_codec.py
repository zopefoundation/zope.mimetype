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
Tests for codec.py.

"""

import unittest

from zope.testing import cleanup

from zope import component


class TestCodecInitialize(cleanup.CleanUp,
                          unittest.TestCase):

    def test_does_nothing_if_codec_registered(self):
        from zope.mimetype import codec
        from zope.mimetype.interfaces import ICodec

        component.provideUtility(self, ICodec)
        codec.initialize(None)

        self.assertEqual(list(component.getUtilitiesFor(ICodec)),
                         [('', self)])
