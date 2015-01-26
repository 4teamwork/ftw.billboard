from DateTime import DateTime
from ftw.billboard.testing import FTW_BILLBOARD_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from unittest2 import TestCase


class TestAdListings(TestCase):

    layer = FTW_BILLBOARD_FUNCTIONAL_TESTING

    def setUp(self):
        self.folder = create(Builder('folder').titled('ads'))
        category = create(Builder('billboard category')
                          .titled('Category')
                          .within(self.folder))

        create(Builder('billboard ad')
               .titled('Expired Ad')
               .having(adExpirationDate=DateTime() - 1)
               .within(category))

        create(Builder('billboard ad')
               .titled('Current Ad')
               .within(category))

    @browsing
    def test_categories_overview_ad_count(self, browser):
        browser.login().visit(self.folder, view='@@category_listing')

        self.assertEquals('1',
                          browser.css('ul.linkListing li span').first.text,
                          'Expect one ad - since only one is visible on '
                          'category listing')
