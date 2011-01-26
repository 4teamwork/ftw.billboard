from Products.Five.browser import BrowserView


class CategoryView(BrowserView):
    """Shows a billboard category."""

    def get_ads(self):
        """returns all ads in this category"""
        catalog = self.context.portal_catalog
        return catalog(dict(
            path = '/'.join(self.context.getPhysicalPath()),
            portal_type = 'BillboardAd',
            sort_on = 'created'))
