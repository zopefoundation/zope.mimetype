=========
 Changes
=========

4.0 (2025-09-12)
================

- Replace ``pkg_resources`` namespace with PEP 420 native namespace.


3.2 (2025-07-03)
================

- Add support for Python 3.13.

- Drop support for Python 3.7, 3.8.


3.1 (2024-02-08)
================

- Add support for Python 3.12.


3.0 (2023-02-27)
================

- Add support for Python 3.9, 3.10, 3.11.

- Drop support for Python 2.7, 3.5, 3.6.

- Drop support for deprecated ``python setup.py test``.


2.5.1 (2021-04-15)
==================

- Fix test compatibility with zope.interface 5.4.


2.5.0 (2020-03-30)
==================

- Add support for Python 3.8.

- Drop support for Python 3.4.

- Ensure all objects have consistent interface resolution orders. See
  `issue 17 <https://github.com/zopefoundation/zope.mimetype/issues/17>`_.


2.4.0 (2018-10-16)
==================

- Add support for Python 3.7.

- Fix DeprecationWarnings for ``IObjectEvent`` and ``ObjectEvent`` by
  importing them from ``zope.interface.interfaces``. See `issue 14
  <https://github.com/zopefoundation/zope.mimetype/issues/14>`_.


2.3.2 (2018-07-30)
==================

- Documentation was moved to https://zopemimetype.readthedocs.io

- Fix an AttributeError accessing the ``preferredCharset`` of an
  ``ICodecTerm`` when no ``ICodecPreferredCharset`` was registered.

- Reach and automatically require 100% test coverage.

2.3.1 (2018-01-09)
==================

- Only try to register the browser stuff in the ZCA when `zope.formlib` is
  available as it breaks otherwise.


2.3.0 (2017-09-28)
==================

- Drop support for Python 3.3.

- Move the dependencies on ``zope.browser``, ``zope.publisher`` and
  ``zope.formlib`` (only needed to use the ``source`` and ``widget``
  modules) into a new ``browser`` extra.
  See `PR 8 <https://github.com/zopefoundation/zope.mimetype/pull/8>`_.

2.2.0 (2017-04-24)
==================

- Fix `issue 6 <https://github.com/zopefoundation/zope.mimetype/issues/6>`_:
  ``typegetter.smartMimeTypeGuesser`` would raise ``TypeError`` on Python 3
  when the data was ``bytes`` and the ``content_type`` was ``text/html``.

- Add support for Python 3.6.


2.1.0 (2016-08-09)
==================

- Add support for Python 3.5.

- Drop support for Python 2.6.

- Fix configuring the package via its included ZCML on Python 3.

2.0.0 (2014-12-24)
==================

- Add support for PyPy and PyPy3.

- Add support for Python 3.4.

- Restore the ability to write ``from zope.mimetype import types``.

- Make ``configure.zcml`` respect the renaming of the ``types`` module
  so that it can be loaded.


2.0.0a1 (2013-02-27)
====================

- Add support for Python 3.3.

- Replace deprecated ``zope.component.adapts`` usage with equivalent
  ``zope.component.adapter`` decorator.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Rename ``zope.mimetype.types`` to ``zope.mimetype.mtypes``.

- Drop support for Python 2.4 and 2.5.


1.3.1 (2010-11-10)
==================

- No longer dependg on ``zope.app.form`` in ``configure.zcml`` by using
  ``zope.formlib`` instead, where the needed interfaces are living now.

1.3.0 (2010-06-26)
==================

- Add testing dependency on ``zope.component[test]``.

- Use zope.formlib instead of zope.app.form.browser for select widget.

- Conform to repository policy.

1.2.0 (2009-12-26)
==================

- Convert functional tests to unit tests and get rid of all extra test
  dependencies as a result.

- Use the ITerms interface from zope.browser.

- Declare missing dependencies, resolved direct dependency on
  zope.app.publisher.

- Import content-type parser from ``zope.contenttype``, adding a dependency on
  that package.

1.1.2 (2009-05-22)
==================

- No longer depend on ``zope.app.component``.

1.1.1 (2009-04-03)
==================

- Fix wrong package version (version ``1.1.0`` was released as ``0.4.0`` at
  `pypi` but as ``1.1dev`` at `download.zope.org/distribution`)

- Fix author email and home page address.

1.1.0 (2007-11-01)
==================

- Package data update.

- First public release.

1.0.0 (2007-??-??)
==================

- Initial release.
