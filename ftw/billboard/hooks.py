from Products.CMFCore.utils import getToolByName
import logging

logger = logging.getLogger('ftw.billboard')

INDEXES = (
    ('get_ad_expiration_date', 'DateIndex'),
)


def imported(site):
    add_catalog_indexes(site, INDEXES)


def add_catalog_indexes(portal, INDEXES):
    """Method to add our wanted indexes to the portal_catalog.
    """

    catalog = getToolByName(portal, 'portal_catalog')
    indexes = catalog.indexes()
    indexables = []

    for name, meta_type in INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)

    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)
