from ftw.billboard.testing import FTW_BILLBOARD_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import login, setRoles
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
import transaction
import unittest2 as unittest


class TestSetup(unittest.TestCase):

    layer = FTW_BILLBOARD_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(self.layer['app'])
        folder = portal[portal.invokeFactory(id='folder',
                                             type_name='Folder')]

        self.bc1 = folder[folder.invokeFactory(
                id='bc1',
                type_name='BillboardCategory')]

        # Update email property
        mtool = getToolByName(self.bc1, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        member.setMemberProperties({'email': 'HUGO.BOSS@4teamwork.ch'})

        transaction.commit()

    def _open_url(self, url):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD))
        self.browser.open(url)

    def test_creation(self):
        self._open_url("%s/createObject?type_name=BillboardAd" % self.bc1.absolute_url())
        # check for email email address
        self.assertEqual(
            self.browser.getControl(name='contactMail').value,
            'hugo.boss@4teamwork.ch')

        self.browser.getControl(name='title').value = 'Ad1'
        self.browser.getControl(name='form.button.save').click()
        self.assertEqual(self.browser.url,
                         'http://nohost/plone/folder/bc1/ad1/')
