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
Tests for source.py.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

from zope import component
from zope.testing import cleanup

from zope.mimetype.interfaces import ICodec
from zope.mimetype.interfaces import ICodecTerm


class TestCodecTerms(cleanup.CleanUp,
                     unittest.TestCase):

    # py2 bwc
    assertRaisesRegex = getattr(unittest.TestCase,
                                'assertRaisesRegex',
                                unittest.TestCase.assertRaisesRegexp)

    def _make_codec_terms(self, source=None):
        try:
            from zope.mimetype.source import CodecTerms
            from zope.mimetype.source import codecSource
        except ImportError: # pragma: no cover
            raise unittest.SkipTest("Missing browser extra")

        return CodecTerms(source if source is not None else codecSource,
                          None)


    def setUp(self):
        from zope.configuration import xmlconfig

        super(TestCodecTerms, self).setUp()

        xmlconfig.string("""
        <configure
            xmlns="http://namespaces.zope.org/zope"
            i18n_domain="zope.mimetype">
          <include package="zope.mimetype" file="meta.zcml" />
          <include package="zope.mimetype" />
          <codec name="iso8859-1" title="Western (ISO-8859-1)">
            <charset name="latin1" />
          </codec>
          <codec name="utf-8" title="UTF-8">
          </codec>
        </configure>
        """)
        self.terms = self._make_codec_terms()

    def test_get_value(self):
        self.assertIsNotNone(self.terms.getValue('iso8859-1'))

    def test_get_value_missing(self):
        with self.assertRaisesRegex(LookupError, "no matching code"):
            self.terms.getValue("Not a codec")

    def test_get_value_not_in_context(self):
        self.terms = self._make_codec_terms({})
        with self.assertRaisesRegex(LookupError, "codec not in source"):
            self.terms.getValue("iso8859-1")

    def test_get_term(self):
        codec = component.getUtility(ICodec, 'iso8859-1')
        term = self.terms.getTerm(codec)

        self.assertTrue(ICodecTerm.providedBy(term))

        self.assertEqual('iso8859-1', term.token)
        self.assertEqual('Western (ISO-8859-1)', term.title)

        self.assertEqual('latin1', term.preferredCharset)


    def test_get_term_no_charset_registered(self):
        codec = component.getUtility(ICodec, 'utf-8')
        term = self.terms.getTerm(codec)

        self.assertTrue(ICodecTerm.providedBy(term))

        self.assertEqual('utf-8', term.preferredCharset)
