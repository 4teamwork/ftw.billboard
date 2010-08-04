from Products.Five.browser import BrowserView
from ftw.table.interfaces import ITableGenerator
from zope.component import getUtility


class CategoryView(BrowserView):
    """Shows a billboard category."""

    def get_elements(self):
        elements = []
        catalog = self.context.portal_catalog
        query = {
            'path': '/'.join(self.context.getPhysicalPath()),
            'portal_type': 'BillboardAd',
        }
        for brain in catalog(query):
            elements.append({
                'Title': '<a href="%s">%s</a>' % (
                    brain.getPath(),
                    brain.Title,
                ),
                'Creator': brain.Creator,
                'end': brain.expires.strftime('%d.%m.%Y'),
            })
        return elements

    def columns(self):
        """Return the names of colums"""
        return (
            'Title',
            'Creator',
            'end',
        )

    def render(self):
        """Return a generated table"""
        generator = getUtility(ITableGenerator, 'ftw.tablegenerator')
        return generator.generate(self.get_elements(), self.columns())
