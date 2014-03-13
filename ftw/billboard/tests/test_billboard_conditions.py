from ftw.billboard.testing import FTW_BILLBOARD_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from unittest2 import TestCase
import transaction


class ReadablePriceTestCase(TestCase):

    layer = FTW_BILLBOARD_FUNCTIONAL_TESTING

    def setUp(self):

        self.category = create(Builder('billboard category')
                               .titled('Category'))

    @browsing
    def test_no_checkbox_on_add_form_if_no_condition_is_set(self, browser):

        browser.login().visit(self.category)
        factoriesmenu.add('BillboardAd')

        self.assertFalse(
            browser.css('#archetypes-fieldname-acceptConditions'),
            'Expect no conditions checkbox.')

        browser.fill({'Title': 'Ad title',
                      'Contact E-Mail': 'some@email.com'}).submit()
        self.assertTrue(browser.css('body.template-billboard_ad_view'),
                        'Expect to be on the billboard ad view.')

    @browsing
    def test_checkbox_on_add_form_if_condition_is_set(self, browser):
        self.category.setConditions('<p>Conditions</p>')
        transaction.commit()

        browser.login().visit(self.category)
        factoriesmenu.add('BillboardAd')

        self.assertTrue(
            browser.css('#archetypes-fieldname-acceptConditions'),
            'Expect conditions checkbox')

        browser.fill({'Title': 'Ad title',
                      'Contact E-Mail': 'some@email.com',
                      'Conditions': True}).submit()

        self.assertTrue(browser.css('body.template-billboard_ad_view'),
                        'Expect to be on the billboard ad view.')

    @browsing
    def test_conditions_required_if_category_has_conditions(self, browser):
        self.category.setConditions('<p>Conditions</p>')
        transaction.commit()

        browser.login().visit(self.category)
        factoriesmenu.add('BillboardAd')

        self.assertTrue(
            browser.css('#archetypes-fieldname-acceptConditions'),
            'Expect conditions checkbox')

        browser.fill({'Title': 'Ad title',
                      'Contact E-Mail': 'some@email.com'}).submit()

        self.assertTrue(browser.css('body.template-atct_edit'),
                        'Expect to be still on the edit page')

        selector = '#archetypes-fieldname-acceptConditions .fieldErrorBox'
        self.assertEquals('Please accept the conditions.',
                          browser.css(selector).first.text)
