TranslatableSourceSelectWidget
==============================

TranslatableSourceSelectWidget is a SourceSelectWidget that translates
and sorts the choices.

We will borrow the boring set up code from the SourceSelectWidget test
(source.txt in zope.formlib).

    >>> import zope.interface
    >>> import zope.component
    >>> import zope.schema
    >>> import zope.schema.interfaces

    >>> @zope.interface.implementer(zope.schema.interfaces.IIterableSource)
    ... class SourceList(list):
    ...     pass

    >>> import base64, binascii
    >>> import zope.publisher.interfaces.browser
    >>> from zope.browser.interfaces import ITerms
    >>> from zope.schema.vocabulary import SimpleTerm
    >>> @zope.interface.implementer(ITerms)
    ... class ListTerms:
    ...
    ...     def __init__(self, source, request):
    ...         pass # We don't actually need the source or the request :)
    ...
    ...     def getTerm(self, value):
    ...         title = value.decode() if isinstance(value, bytes) else value
    ...         try:
    ...             token = base64.b64encode(title.encode()).strip().decode()
    ...         except binascii.Error:
    ...             raise LookupError(token)
    ...         return SimpleTerm(value, token=token, title=title)
    ...
    ...     def getValue(self, token):
    ...         return token.decode('base64')

    >>> zope.component.provideAdapter(
    ...     ListTerms,
    ...     (SourceList, zope.publisher.interfaces.browser.IBrowserRequest))

    >>> dog = zope.schema.Choice(
    ...    __name__ = 'dog',
    ...    title=u"Dogs",
    ...    source=SourceList(['spot', 'bowser', 'prince', 'duchess', 'lassie']),
    ...    )
    >>> dog = dog.bind(object())

Now that we have a field and a working source, we can construct and render
a widget.

    >>> from zope.mimetype.widget import TranslatableSourceSelectWidget
    >>> from zope.publisher.browser import TestRequest
    >>> request = TestRequest()
    >>> widget = TranslatableSourceSelectWidget(
    ...     dog, dog.source, request)

    >>> print(widget())
    <div>
    <div class="value">
    <select id="field.dog" name="field.dog" size="5" >
    <option value="Ym93c2Vy">bowser</option>
    <option value="ZHVjaGVzcw==">duchess</option>
    <option value="bGFzc2ll">lassie</option>
    <option value="cHJpbmNl">prince</option>
    <option value="c3BvdA==">spot</option>
    </select>
    </div>
    <input name="field.dog-empty-marker" type="hidden" value="1" />
    </div>

Note that the options are ordered alphabetically.

If the field is not required, we will also see a special choice labeled
"(nothing selected)" at the top of the list

    >>> dog.required = False
    >>> print(widget())
    <div>
    <div class="value">
    <select id="field.dog" name="field.dog" size="5" >
    <option selected="selected" value="">(nothing selected)</option>
    <option value="Ym93c2Vy">bowser</option>
    <option value="ZHVjaGVzcw==">duchess</option>
    <option value="bGFzc2ll">lassie</option>
    <option value="cHJpbmNl">prince</option>
    <option value="c3BvdA==">spot</option>
    </select>
    </div>
    <input name="field.dog-empty-marker" type="hidden" value="1" />
    </div>
