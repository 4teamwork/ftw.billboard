from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class CategoryView(BrowserView):
    """Shows a billboard category."""

    template = ViewPageTemplateFile("category.pt")

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if not member.has_permission('Modify portal content', self.context):
            self.request.set('disable_border', 1)
        return self.template()

    def get_ads(self):
        """Returns all ads in this category."""
        context = aq_inner(self.context)
        ct = getToolByName(context, 'portal_catalog')

        # TODO: make it configurable if ads in all translated categories
        # should be shown.
        if not hasattr(context, 'getTranslations'):
            return ct(
                path='/'.join(self.context.getPhysicalPath()),
                portal_type='BillboardAd',
                sort_on='created',
                sort_order='descending')
        else:
            translations = context.getTranslations().values()
            paths = ['/'.join(t[0].getPhysicalPath()) for t in translations]
            return ct(
                path=paths,
                portal_type='BillboardAd',
                Language='all',
                sort_on='created',
                sort_order='descending')
