"""Definition of the BillboardAd content type
"""

from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.CMFCore.permissions import ManagePortal
from ftw.billboard import billboardMessageFactory as _
from ftw.billboard.config import PROJECTNAME
from ftw.billboard.interfaces import IBillboardAd
from zope.interface import implements
import datetime

BillboardAdSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.TextField('details',
        searchable = True,
        required = False,
        default_content_type = 'text/html',
        default_output_type = 'text/html',
        storage = atapi.AnnotationStorage(),
        widget = atapi.RichWidget(
            label = _(u"billboard_label_details", default=u"Details"),
            description = _(u"billboard_help_details", default=u""),
        ),
    ),

    atapi.StringField(
        name='price',
        storage=atapi.AnnotationStorage(),
        schemata='default',
        required=False,
        widget=atapi.StringWidget(
            label=_(u'billboard_label_price', default='price'),
            description=_(u'billboard_help_price', default=''),
        ),
    ),

    atapi.StringField(
        name='contactMail',
        storage=atapi.AnnotationStorage(),
        schemata='default',
        required=True,
        default_method='getDefaultContactMail',
        widget=atapi.StringWidget(
            label=_(u'billboard_label_contactmail', default='Contact E-Mail'),
            description=_(u'billboard_help_contactmail', default=''),
            i18n_domain='ftw.billboard',
        ),
    ),

    atapi.StringField(
        name='contactPhone',
        storage=atapi.AnnotationStorage(),
        schemata='default',
        required=False,
        widget=atapi.StringWidget(
            label=_(u'billboard_label_contactphone', default='Contact Phone'),
            description=_(u'billboard_help_contactphone', default=''),
        ),
    ),

    atapi.StringField(
        name='contactURL',
        storage=atapi.AnnotationStorage(),
        schemata='default',
        required=False,
        default_method='getDefaultContactURL',
        widget=atapi.StringWidget(
            label=_(u'billboard_label_contacturl', default='Contact URL'),
            description=_(u'billboard_help_contacturl', default=''),
        ),
    ),
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BillboardAdSchema['title'].storage = atapi.AnnotationStorage()
BillboardAdSchema['title'].searchable = True
BillboardAdSchema['title'].required = True
BillboardAdSchema['description'].widget.visible = False
BillboardAdSchema['excludeFromNav'].default = True
BillboardAdSchema['expirationDate'].required = True
BillboardAdSchema['expirationDate'].default_method = 'getDefaultExpirationDate'
BillboardAdSchema['effectiveDate'].write_permission = ManagePortal

if 'showTitle' in BillboardAdSchema:
    del BillboardAdSchema['showTitle']
if 'imageClickable' in BillboardAdSchema:
    del BillboardAdSchema['imageClickable']
if 'image' in BillboardAdSchema:
    del BillboardAdSchema['image']
if 'imageAltText' in BillboardAdSchema:
    del BillboardAdSchema['imageAltText']
if 'imageLayout' in BillboardAdSchema:
    del BillboardAdSchema['imageLayout']

schemata.finalizeATCTSchema(BillboardAdSchema,
                            folderish=True,
                            moveDiscussion=False)

BillboardAdSchema.changeSchemataForField('expirationDate', 'default')
if 'text' in BillboardAdSchema:
    BillboardAdSchema.moveField('text', pos='bottom')
    BillboardAdSchema['text'].widget.label = _(u'Details')
    BillboardAdSchema['text'].widget.rows = 10


class BillboardAd(folder.ATFolder):
    """Billboard Ad"""
    security = ClassSecurityInfo()
    implements(IBillboardAd)

    portal_type = "BillboardAd"
    schema = BillboardAdSchema

    title = atapi.ATFieldProperty('title')
    text = atapi.ATFieldProperty('text')
    contactMail = atapi.ATFieldProperty('contactMail')
    contactURL = atapi.ATFieldProperty('contactURL')
    contactPhone = atapi.ATFieldProperty('contactPhone')

    def getDefaultExpirationDate(self):
        """Return the default expiration date, now + 1 month."""
        now = datetime.datetime.now()
        # + one month (4 weeks)
        date = now + datetime.timedelta(weeks=+4)
        datetuple = date.timetuple()
        return DateTime(*datetuple[:-3])

    def getDefaultContactMail(self):
        """Return the mail of the logged-in user"""
        member = self.portal_membership.getAuthenticatedMember()
        return member.getProperty('email','')

    def getDefaultContactURL(self):
        """Return the URL of the logged-in user"""
        member = self.portal_membership.getAuthenticatedMember()
        return member.getProperty('home_page','')

atapi.registerType(BillboardAd, PROJECTNAME)
