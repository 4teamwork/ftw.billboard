from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class AdView(BrowserView):
    """Shows a billboard ad."""

    template=ViewPageTemplateFile("ad.pt")

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if not member.has_permission('Manage portal', self.context):
            self.request.set('disable_border', 1)
        return self.template()

    def get_elements(self):
        elements = []
        catalog = self.context.portal_catalog
        query = {
            'path': '/'.join(self.context.getPhysicalPath()),
            'portal_type': 'Image',
        }
        for brain in catalog(query):
            elements.append(brain.getPath())
        return elements

    def get_files(self):
        elements = []
        catalog = self.context.portal_catalog
        query = {
            'path': '/'.join(self.context.getPhysicalPath()),
            'portal_type': 'File',
        }
        for brain in catalog(query):
            obj = brain.getObject()
            elements.append({
                'title': brain.Title,
                'path': '%s/at_download/file' % brain.getPath(),
                'icon': obj.getIcon(),
            })
        return elements