from Products.Five.browser import BrowserView

class AdView(BrowserView):
    """Shows a billboard ad."""
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