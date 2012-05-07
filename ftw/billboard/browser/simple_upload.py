import os
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from ftw.billboard import billboardMessageFactory as _
from zope.app.container.interfaces import INameChooser


class AddFile(BrowserView):
    """Form to upload a file"""

    template = ViewPageTemplateFile("simple_upload.pt")
    allowed_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
    create_type = 'File'
    field_name = 'file'
    view_name = 'add_file'

    def __call__(self):
        self.request.set('disable_border', 1)
        if self.request.form.get('form.submitted', None):
            status = IStatusMessage(self.context.REQUEST)
            upload_file = self.request.form.get('upload_file', None)
            error = self.is_wrong_type(upload_file)
            if error:
                status.addStatusMessage(error, type='error')
                return self.template()
            chooser = INameChooser(self.context)
            file_id = chooser.chooseName(upload_file.filename, self)
            self.context.invokeFactory(self.create_type,
                                       file_id,
                                       title=upload_file.filename)
            new_file = self.context.get(file_id)
            new_file.getField(self.field_name).set(new_file, upload_file)
            return self.request.response.redirect('.')
        return self.template()

    def is_wrong_type(self, upload):
        if not upload:
            return _(u'label_required', default=u'Required field')
        else:
            _root, extension = os.path.splitext(upload.filename)
            if extension not in self.allowed_extensions:
                return _(
                    u'label_notallowedtype',
                    default=u'Not allowed type (${types})',
                    mapping={u'types': ', '.join(self.allowed_extensions)})
        return False


class AddImage(AddFile):
    """Form to upload an image"""

    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    create_type = 'Image'
    field_name = 'image'
    view_name = 'add_image'
