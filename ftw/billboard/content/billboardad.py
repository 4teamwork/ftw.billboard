"""Definition of the BillboardAd content type
"""
from AccessControl import ClassSecurityInfo
from DateTime import DateTime

from ftw.billboard import billboardMessageFactory as _
from ftw.billboard import validators
from ftw.billboard.config import PROJECTNAME
from ftw.billboard.interfaces import IBillboardAd

from Products.CMFCore.permissions import ManagePortal
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.validation.config import validation
from zope.interface import implements


validation.register(validators.MailValidator('isEmail'))

BillboardAdSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.TextField('description',
        searchable = True,
        required = False,
        default_content_type = 'text/html',
        default_output_type = 'text/html',
        storage = atapi.AnnotationStorage(),
        widget = atapi.RichWidget(
            label = _(u"label_description", default=u"Description"),
            description = _(u"billboard_help_description", default=u""),
        ),
    ),

    atapi.FixedPointField(
        name='price',
        schemata='default',
        required=False,
        widget=atapi.DecimalWidget(
            label=_(u'label_price', default='price'),
            description=_(u'help_price', default='Leave blank '),
        ),
    ),

    atapi.StringField(
        name='contactMail',
        schemata='default',
        required=True,
        validators=('isEmail'),
        default_method='getDefaultContactMail',
        widget=atapi.StringWidget(
            label=_(u'label_contactmail', default='Contact E-Mail'),
            description=_(u'help_contactmail', default=''),
            i18n_domain='ftw.billboard',
        ),
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BillboardAdSchema['title'].searchable = True
BillboardAdSchema['title'].required = True
BillboardAdSchema['excludeFromNav'].default = True
BillboardAdSchema['expirationDate'].default_method = 'getDefaultExpirationDate'
BillboardAdSchema['effectiveDate'].default_method = DateTime

# hide other schematas
BillboardAdSchema['allowDiscussion'].write_permission = ManagePortal
BillboardAdSchema['excludeFromNav'].write_permission = ManagePortal
BillboardAdSchema['nextPreviousEnabled'].write_permission = ManagePortal
BillboardAdSchema['subject'].write_permission = ManagePortal
BillboardAdSchema['relatedItems'].write_permission = ManagePortal
BillboardAdSchema['location'].write_permission = ManagePortal
BillboardAdSchema['language'].write_permission = ManagePortal
BillboardAdSchema['effectiveDate'].write_permission = ManagePortal
BillboardAdSchema['expirationDate'].write_permission = ManagePortal
BillboardAdSchema['creation_date'].write_permission = ManagePortal
BillboardAdSchema['modification_date'].write_permission = ManagePortal
BillboardAdSchema['creators'].write_permission = ManagePortal
BillboardAdSchema['contributors'].write_permission = ManagePortal
BillboardAdSchema['rights'].write_permission = ManagePortal


schemata.finalizeATCTSchema(BillboardAdSchema,
                            folderish=True,
                            moveDiscussion=False)


class BillboardAd(folder.ATFolder):
    """Billboard Ad"""
    security = ClassSecurityInfo()
    implements(IBillboardAd)

    portal_type = "BillboardAd"
    schema = BillboardAdSchema

    details = atapi.ATFieldProperty('details')

    def getDefaultExpirationDate(self):
        """Return the default expiration date, now + 1 month."""
        return DateTime() + 31

    def getDefaultContactMail(self):
        """Return the mail of the logged-in user"""
        member = self.portal_membership.getAuthenticatedMember()
        return member.getProperty('email','')

    def getDefaultContactName(self):
        """Return the URL of the logged-in user"""
        member = self.portal_membership.getAuthenticatedMember()
        fullname = member.getProperty('fullname','')
        firstname = member.getProperty('firstname','')
        lastname = member.getProperty('lastname','')
        if fullname:
            return fullname
        elif fullname or lastname:
            return ' '.join([firstname, lastname])
        return

atapi.registerType(BillboardAd, PROJECTNAME)