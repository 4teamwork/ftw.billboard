from ftw.billboard.hooks import INDEXES
from ftw.upgrade import UpgradeStep
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
        indexes = catalog.indexes()
        for name, meta_type in INDEXES:
            if name not in indexes:
                catalog.addIndex(name, meta_type)

        query = {'portal_type': 'BillboardAd'}
        for obj in self.objects(query, 'Reindex BillboardAds'):
            if obj.getExpirationDate():  # prevent deletion on mult. executions
                obj.setAdExpirationDate(obj.getExpirationDate())
            obj.setExpirationDate(None)
            obj.reindexObject()
