from ftw.billboard import billboardMessageFactory as _
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IActionsPortlet(IPortletDataProvider):
    """
    """


class Assignment(base.Assignment):
    implements(IActionsPortlet)

    @property
    def title(self):
        return _(
            u'label_billboardactions',
            default=u'Billboard Actions portlet')


class Renderer(base.Renderer):

    def update(self):
        member = self.context.portal_membership.getAuthenticatedMember()
        self.can_add = member.has_permission(
            'ftw.billboard: Add BillboardAd',
            self.context) and self.context.portal_type=='BillboardCategory'

        self.can_edit = member.has_permission(
            'Modify portal content',
            self.context) and self.context.portal_type=='BillboardAd'

        self.can_del = member.has_permission(
            'Delete objects',
            self.context) and self.context.portal_type=='BillboardAd'

    def available(self):
        return self.can_add or self.can_edit or self.can_del
        return not self.context.checkCreationFlag()

    render = ViewPageTemplateFile('actions.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
