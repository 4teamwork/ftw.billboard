from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.billboard.helpers import format_currency
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class AdView(BrowserView):
    """Shows a billboard ad."""

    template = ViewPageTemplateFile("ad.pt")

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if not member.has_permission('Manage portal', self.context):
            self.request.set('disable_border', 1)
        return self.template()

    def can_edit(self):
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission('Modify portal content', self.context)

    def get_elements(self):
        elements = []
        catalog = self.context.portal_catalog
        query = {
            'path': '/'.join(self.context.getPhysicalPath()),
            'portal_type': 'Image',
            }
        for brain in catalog(query):
            elements.append(brain.getURL())
        return elements

    def get_files(self):
        files = []
        catalog = self.context.portal_catalog
        query = {
            'path': '/'.join(self.context.getPhysicalPath()),
            'portal_type': 'File',
            }
        for brain in catalog(query):
            files.append(dict(
                    title=brain.Title,
                    url=brain.getURL()))
        return files

    def get_readable_price(self):
        registry = getUtility(IRegistry)
        currency = registry.records['ftw.billboard.currency']
        decimal_mark = registry.records['ftw.billboard.decimalmark']
        thousandsseperator = registry.records[
            'ftw.billboard.thousandsseparator']
        formated_value = format_currency(self.context.getPrice(),
            decimal_mark=decimal_mark.value,
            thousands_separator=thousandsseperator.value)
        return formated_value + ' ' + currency.value
