from ftw.upgrade import UpgradeStep
from ftw.billboard.hooks import add_catalog_indexes
from ftw.billboard.hooks import INDEXES
from Products.CMFCore.utils import getToolByName


class AddExpirationDate(UpgradeStep):
    """ Moves value from expirationDate to adExpirationDate.
        Creates index for the new field.
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.calendarwidget:default')
        self.setup_install_profile(
            'profile-ftw.billboard.upgrades:1221')

        catalog = getToolByName(self.portal, 'portal_catalog')
        brains = catalog(portal_type='BillboardAd')
        objs = [brain.getObject() for brain in brains]
        for obj in objs:
            if obj.getExpirationDate():  # prevent deletion on mult. executions
                obj.setAdExpirationDate(obj.getExpirationDate())
            obj.setExpirationDate(None)
            obj.reindexObject()

        add_catalog_indexes(self.portal, INDEXES)
