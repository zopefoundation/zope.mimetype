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
from __future__ import absolute_import

import codecs
import os
import re

from zope import interface, component
from zope.mimetype.interfaces import ICodec, ICharsetCodec
from zope.mimetype.interfaces import ICharset, ICodecPreferredCharset


@interface.implementer(ICodec)
class Codec(object):

    def __init__(self, name, title):
        self.name = name
        self.title = title
        ( self.encode,
          self.decode,
          self.reader,
          self.writer
          ) = codecs.lookup(name)


def addCodec(name, title=None):
    codec = Codec(name, title)
    component.provideUtility(codec, provides=ICodec, name=name)


@interface.implementer(ICharset)
class Charset(object):

    def __init__(self, name, encoding):
        self.name = name
        self.encoding = encoding


def addCharset(encoding, name, preferred=False):
    codec = component.getUtility(ICodec, name=encoding)
    charset = Charset(name, codec.name)
    component.provideUtility(charset, provides=ICharset, name=name)
    interface.alsoProvides(codec, ICharsetCodec)
    component.provideUtility(codec, provides=ICharsetCodec, name=name)
    if preferred:
        utility = component.queryUtility(
            ICodecPreferredCharset, name=codec.name)
        if utility is not None:
            raise ValueError("Codec already has a preferred charset.")
        interface.alsoProvides(charset, ICodecPreferredCharset)
        component.provideUtility(
            charset, provides=ICodecPreferredCharset, name=codec.name)


FILENAME = "character-sets.txt"

DATA_RE = re.compile(
    r'(Name|Alias|MIBenum):\s*(\S+)\s*(\(preferred MIME name\))?'
    )

def initialize(_context):
    # if any ICodec has been registered, we're done:
    for _ in component.getUtilitiesFor(ICodec):
        return
    _names = []
    _codecs = {}
    _aliases = {} # alias -> codec name
    here = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(here, FILENAME)
    f = open(fn, "r")

    class Codec(object):
        preferred_alias = None

        def __init__(self, name):
            self.name = name
            self.aliases = [name.lower()]

        def findPyCodecs(self):
            self.pyCodecs = {}
            for alias in self.aliases:
                try:
                    codec = codecs.lookup(alias)
                except LookupError:
                    pass
                else:
                    self.pyCodecs[alias] = codec

    for line in f:
        if not line.strip():
            lastname = None
            continue
        m = DATA_RE.match(line)
        if m is None:
            continue

        type, name, preferred = m.groups()
        if type == "Name":
            if name in _codecs: # pragma: no cover (its our datafile, this shouldn't happen)
                raise ValueError("codec %s already exists" % name)
            _names.append(name)
            lastname = name
            _codecs[name] = Codec(name)
            if preferred:
                _codecs[name].preferred_alias = name.lower()

        elif type == "Alias" and name != "None":
            if not lastname: # pragma: no cover (its our datafile, this shouldn't happen)
                raise ValueError("Parsing failed. Alias found without a name.")
            name = name.lower()
            if name in _aliases: # pragma: no cover (its our datafile, this shouldn't happen)
                raise ValueError("Alias %s already exists." % name)
            codec = _codecs[lastname]
            codec.aliases.append(name)
            _aliases[name] = lastname
            if preferred:
                codec.preferred_alias = name

    f.close()
    for name in _names:
        codec = _codecs[name]
        codec.findPyCodecs()
        if codec.pyCodecs.get(codec.preferred_alias):
            pyName = codec.preferred_alias
        else:
            for pyName in codec.aliases:
                if pyName in codec.pyCodecs:
                    break
            else:
                continue # not found under any name
        _context.action(
            discriminator=None,
            callable=addCodec,
            args=(pyName, codec.name),
            )
        if not codec.preferred_alias:
            codec.preferred_alias = codec.aliases[0]
        for alias in codec.aliases:
            _context.action(
                discriminator=(pyName, alias),
                callable=addCharset,
                args=(pyName, alias, alias == codec.preferred_alias)
                )
