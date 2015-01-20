from ftw.billboard.interfaces import IBillboardAd
from plone.indexer import indexer


@indexer(IBillboardAd)
def get_ad_expiration_date(obj):
    return obj.getAdExpirationDate()
