from ftw.billboard.portlets import actions
from ftw.billboard.testing import FTW_BILLBOARD_INTEGRATION_TESTING
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from zope.component import getUtility, getMultiAdapter
import unittest2 as unittest


class TestPortlet(unittest.TestCase):
    """ Basic tests for the recentlymodifiedportlet
    """

    layer = FTW_BILLBOARD_INTEGRATION_TESTING

    def testInterfaces(self):
        portlet = actions.Assignment()
        self.failUnless(
            actions.IActionsPortlet.providedBy(portlet))

    def testRenderer(self):
        context = self.layer['portal']
        request = self.layer['request']
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn', context=context)
        assignment = actions.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)

        self.failUnless(isinstance(renderer, actions.Renderer))
