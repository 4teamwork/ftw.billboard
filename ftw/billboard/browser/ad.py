from Products.Five.browser import BrowserView
from ftw.workspace.browser import helper as workspace_helper

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
            Test = brain.getObject()
            height = int(round(200*float(Test.height)/float(Test.width), 0))
            height = str(height)
            elements.append({
                'Title': '<a href="%s"><img width="200" height="%s" src="%s"</a>' % (
                    brain.getPath(),
                    height,
                    brain.getPath(),
                ),
                'Creator': brain.Creator,
                'end': brain.expires.strftime('%d.%m.%Y'),
            })
        return elements

    def get_files(self):
        elements = []
        catalog = self.context.portal_catalog
        query = {
            'path': '/'.join(self.context.getPhysicalPath()),
            'portal_type': 'File',
        }
        for brain in catalog(query):
            File = brain.getObject()            
            elements.append({
                'Title': workspace_helper.icon(brain,File.getContentType()) + '<a href="%s">%s</a>' % (
                                     brain.getPath() + "/at_download/file",
                                     brain.Title,
                                 ),
                                 'Creator': brain.Creator,
                                 'end': brain.expires.strftime('%d.%m.%Y'),
                                 'icon': workspace_helper.icon(File,File.getContentType()),
            
            })
        return elements