from Products.CMFCore.utils import getToolByName
from ftw.billboard.testing import FTW_BILLBOARD_INTEGRATION_TESTING
import unittest2 as unittest

class ReadablePriceTestCase(unittest.TestCase):
    layer = FTW_BILLBOARD_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        portal.invokeFactory('Folder', 'f1')
        self.folder = portal['f1']
        self.folder.invokeFactory('BillboardCategory', 'bc1')
        self.cat = self.folder['bc1']
        self.cat.invokeFactory('BillboardAd', 'ad')
        self.ad = self.cat['ad']

    def test_default(self):
        portal = self.layer['portal']
        self.ad.price = '3485.55'
        ad_view = portal.restrictedTraverse('/'.join(
                self.ad.getPhysicalPath()) + '/billboard_ad_view')
        readable_price = ad_view.get_readable_price()
        self.assertEqual(readable_price, "3'485.55 SFr.")

    def test_changed(self):
        portal = self.layer['portal']
        registry = getToolByName(portal, 'portal_registry')
        registry.records['ftw.billboard.currency'].value = u'\u20ac'
        registry.records['ftw.billboard.decimalmark'].value = u','
        registry.records['ftw.billboard.thousandsseparator'].value = u'.'
        self.ad.price = '3485.55'
        ad_view = portal.restrictedTraverse('/'.join(
                self.ad.getPhysicalPath()) + '/billboard_ad_view')
        readable_price = ad_view.get_readable_price()
        self.assertEqual(readable_price, u"3.485,55 \u20ac")
