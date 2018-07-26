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
Tests for zcml.py

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

from zope import component
from zope.configuration import xmlconfig
from zope.testing import cleanup

class TestCodecDirective(cleanup.CleanUp,
                         unittest.TestCase):

    def test_codec(self):
        from zope.mimetype.interfaces import ICodec
        from zope.mimetype.interfaces import ICharset

        xmlconfig.string("""
        <configure
            xmlns="http://namespaces.zope.org/zope"
            i18n_domain="zope.mimetype">
          <include package="zope.mimetype" file="meta.zcml" />
          <codec name="iso8859-1" title="Western (ISO-8859-1)">
            <charset name="latin1" />
          </codec>
        </configure>
        """)

        codec = component.getUtility(ICodec, "iso8859-1")
        self.assertEqual("Western (ISO-8859-1)", codec.title)

        charset = component.getUtility(ICharset, "latin1")
        self.assertIsNotNone(charset)


class TestMimeTypesDirective(cleanup.CleanUp,
                             unittest.TestCase):

    def test_create_interfaces(self):
        import os
        import sys
        import types

        fake_module = types.ModuleType("zope_mime_testing")
        sys.modules[fake_module.__name__] = fake_module
        path = os.path.join(os.path.dirname(__file__), '..', 'types.csv')
        try:
            xmlconfig.string("""
            <configure
                xmlns="http://namespaces.zope.org/zope"
                i18n_domain="zope.mimetype">
              <include package="zope.mimetype" file="meta.zcml" />
              <mimeTypes file='%s' module="zope_mime_testing" />
            </configure>
            """ % (path,))
        finally:
            del sys.modules[fake_module.__name__]

        self.assertTrue(hasattr(fake_module, 'IContentTypeCSV'))
