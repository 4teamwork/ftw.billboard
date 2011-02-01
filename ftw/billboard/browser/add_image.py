from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from ftw.billboard import billboardMessageFactory as _
from zope.app.container.interfaces import INameChooser

class AddImage(BrowserView):
    """Form to upload an image"""

    template=ViewPageTemplateFile("add_image.pt")

    def __call__(self):
        allowed_types = ['image/jpeg', 'image/gif', 'image/png']
        if self.request.form.get('form.submitted', None):
            status = IStatusMessage(self.context.REQUEST)
            img = self.request.form.get('img', None)
            chooser = INameChooser(self.context)
            if not img:
                status.addStatusMessage(
                    _(u'label_no_image', default=u'Not an image'),
                    type='error')
                return self.template()
            if img.headers.dict['content-type'] not in allowed_types:
                status.addStatusMessage(
                    _(u'label_not_image', default=u'Not allowd content type'),
                    type='error')
                return self.template()
            img_id = chooser.chooseName(img.filename, self)
            self.context.invokeFactory('Image', img_id)
            new_img = self.context.get(img_id)
            new_img.getField('image').set(new_img, img)
            return self.request.response.redirect('.')
        return self.template()
