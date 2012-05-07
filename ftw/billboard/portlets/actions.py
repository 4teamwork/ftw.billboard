from Acquisition import aq_inner
from ftw.billboard import billboardMessageFactory as _
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IActionsPortlet(IPortletDataProvider):
    """Actions portlet interface.
    """


class Assignment(base.Assignment):
    implements(IActionsPortlet)

    @property
    def title(self):
        return _(
            u'label_billboardactions',
            default=u'Billboard Actions portlet')


class Renderer(base.Renderer):

    def __init__(self, *args, **kwargs):
        super(Renderer, self).__init__(*args, **kwargs)
        self.can_add = False
        self.can_edit = False
        self.can_del = False
        self.allowed_types = []

    def update(self):
        context = aq_inner(self.context)
        mtool = getMultiAdapter((context, self.request),
                         name=u'plone_tools').membership()

        self.can_add = mtool.checkPermission('ftw.billboard: Add BillboardAd',
            context) and context.portal_type == 'BillboardCategory'

        self.can_edit = mtool.checkPermission('Modify portal content',
            context) and context.portal_type == 'BillboardAd'

        self.can_del = mtool.checkPermission('Delete objects',
            context) and context.portal_type == 'BillboardAd'

        self.allowed_types = [term.id for term in
                             self.context.allowedContentTypes()]

    def available(self):
        if self.context.checkCreationFlag():
            return False
        return self.can_add or self.can_edit or self.can_del

    render = ViewPageTemplateFile('actions.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
