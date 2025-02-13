Package configuration
=====================

The ``zope.mimetype`` package provides a ZCML file that configures some
adapters and utilities and a couple of views:

  >>> from zope.configuration.xmlconfig import XMLConfig
  >>> import zope.mimetype

  >>> len(list(zope.component.getGlobalSiteManager().registeredUtilities()))
  0

  >>> XMLConfig('configure.zcml', zope.mimetype)()

  >>> len(list(zope.component.getGlobalSiteManager().registeredUtilities())) >= 755
  True


The 'zmi_icon' adapters are only installed if zope.browserresource
is available:

  >>> try:
  ...    import zope.browserresource
  ... except ModuleNotFoundError:
  ...    expected = 1
  ... else:
  ...    expected = 107
  >>> len(list(zope.component.getGlobalSiteManager().registeredAdapters())) == expected
  True
