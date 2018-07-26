"""Widget that provides translation and sorting for an IIterableSource.

This widget translates the term titles and presents those in sorted order.

Properly, this should call on a language-specific collation routine,
but we don't currently have those.  Also, it would need to deal with a
partially-translated list of titles when translations are only
available for some of the titles.

The implementation ignores these issues for now.

"""
from __future__ import absolute_import

__docformat__ = "reStructuredText"

import zope.formlib.source
import zope.i18n


class TranslatableSourceSelectWidget(
        zope.formlib.source.SourceSelectWidget):

    def __init__(self, field, source, request):
        super(TranslatableSourceSelectWidget, self).__init__(
            field, source, request)
        self.displays = {}   # value --> (display, token)
        self.order = []      # values in sorted order

        # XXX need a better way to sort in an internationalized context
        sortable = []
        for value in source:
            t = self.vocabulary.terms.getTerm(value)
            title = zope.i18n.translate(t.title, context=request)
            self.displays[value] = title, t.token
            lower = title.lower()
            sortable.append((lower, value))
        sortable.sort()
        self.order = [value for (lower, value) in sortable]

    def renderItemsWithValues(self, values):
        """Render the list of possible values, with those found in
        `values` being marked as selected."""

        cssClass = self.cssClass

        # multiple items with the same value are not allowed from a
        # vocabulary, so that need not be considered here
        rendered_items = []
        count = 0

        # Handle case of missing value
        missing = self._toFormValue(self.context.missing_value)

        if self._displayItemForMissingValue and not self.context.required:
            render = self.renderSelectedItem if missing in values else self.renderItem

            missing_item = render(
                count,
                self.translate(self._messageNoValue),
                missing,
                self.name,
                cssClass)
            rendered_items.append(missing_item)
            count += 1

        # Render normal values
        for value in self.order:
            item_text, token = self.displays[value]

            render = self.renderSelectedItem if value in values else self.renderItem

            rendered_item = render(
                count,
                item_text,
                token,
                self.name,
                cssClass)

            rendered_items.append(rendered_item)
            count += 1

        return rendered_items

    def textForValue(self, term):
        return self.displays[term.value]


class TranslatableSourceDropdownWidget(TranslatableSourceSelectWidget):

    size = 1
