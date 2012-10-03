from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.CMFCore.permissions import View
from Products.validation import V_REQUIRED
from Products.validation.config import validation
from Products.validation.validators.SupplValidators import MaxSizeValidator
from ftw.billboard import billboardMessageFactory as _
from ftw.billboard.config import PROJECTNAME
from ftw.billboard.interfaces import IBillboardCategory
from zope.interface import implements


validation.register(MaxSizeValidator('checkImageMaxSize',
                                     maxsize=zconf.ATImage.max_file_size))


BillboardCategorySchema = folder.ATFolderSchema.copy() + atapi.Schema((
        atapi.ImageField(
            name='image',
            required=False,
            primary=True,
            languageIndependent=True,
            storage=atapi.AnnotationStorage(),
            swallowResizeExceptions=zconf.swallowImageResizeExceptions.enable,
            pil_quality=zconf.pil_config.quality,
            pil_resize_algo=zconf.pil_config.resize_algo,
            max_size=zconf.ATImage.max_image_dimension,

            sizes={'large': (768, 768),
                   'preview': (400, 400),
                   'mini': (200, 200),
                   'thumb': (128, 128),
                   'tile': (64, 64),
                   'icon': (32, 32),
                   'listing': (16, 16),
                   },

            validators=(
                ('isNonEmptyFile', V_REQUIRED),
                ('checkImageMaxSize', V_REQUIRED)),
            widget=atapi.ImageWidget(
                label=_(u"label_image", default=u"Image"),
                show_content_type=False,
                )
            ),
        ))
# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(BillboardCategorySchema,
                            folderish=True,
                            moveDiscussion=False)


class BillboardCategory(folder.ATFolder):
    """A type for billboard categories."""
    implements(IBillboardCategory)
    schema = BillboardCategorySchema

    image = atapi.ATFieldProperty('image')

    security = ClassSecurityInfo()
    security.declareProtected(View, 'tag')

    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return folder.ATFolder.__bobo_traverse__(self, REQUEST, name)

atapi.registerType(BillboardCategory, PROJECTNAME)
