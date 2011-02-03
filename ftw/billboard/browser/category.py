from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class CategoryView(BrowserView):
    """Shows a billboard category."""

    template=ViewPageTemplateFile("category.pt")

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if not member.has_permission('Modify portal content', self.context):
            self.request.set('disable_border', 1)
        return self.template()

    def get_ads(self):
        """returns all ads in this category"""
        catalog = self.context.portal_catalog
        return catalog(dict(
            path = '/'.join(self.context.getPhysicalPath()),
            portal_type = 'BillboardAd',
            sort_on = 'created'))
