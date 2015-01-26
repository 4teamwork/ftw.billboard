from DateTime import DateTime
from ftw.billboard.testing import FTW_BILLBOARD_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from unittest2 import TestCase


class TestAdListings(TestCase):

    layer = FTW_BILLBOARD_FUNCTIONAL_TESTING

    def setUp(self):
        self.category = create(Builder('billboard category')
                               .titled('Category'))

        self.expired_ad = create(Builder('billboard ad')
                                 .titled('Expired Ad')
                                 .having(adExpirationDate=DateTime()-1)
                                 .within(self.category))

        self.current_ad = create(Builder('billboard ad')
                                 .titled('Current Ad')
                                 .within(self.category))

    @browsing
    def test_only_non_expired_ads_are_displayed_in_category_listing(self, browser):
        browser.login().visit(self.category)
        ads = browser.css('.billboardAdsListing tr')

        self.assertEquals(1,
                          len(ads))

        self.assertEquals('Current Ad',
                          ads.first.css('td:last-child').first.text)

    @browsing
    def test_my_ads_also_list_expired_ads(self, browser):
        browser.login().visit(self.category, view='my_ads')
        ads = browser.css('.billboardAdsListing tr')

        self.assertEquals(2,
                          len(ads))

        # tests if the expired ad is also present
        self.assertEquals('Expired Ad expired',
                          ads.first.css('td:last-child').first.text)
