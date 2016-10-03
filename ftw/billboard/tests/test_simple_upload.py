from ftw.billboard.browser.simple_upload import AddFile
from ftw.billboard.testing import FTW_BILLBOARD_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from unittest2 import TestCase


class DummyFile(object):

    filename = ''

    def __init__(self, filename):
        self.filename = filename


class TestSimpleUpload(TestCase):

    layer = FTW_BILLBOARD_FUNCTIONAL_TESTING

    @browsing
    def test_is_wrong_type_returns_true_if_extension_is_not_allowed(self, browser):
        add_file = AddFile(object, object)
        add_file.allowed_extensions = ['.my_extension']

        file_ = DummyFile('james.my_bad_extension')

        self.assertTrue(add_file.is_wrong_type(file_))

    @browsing
    def test_is_wrong_type_is_case_insensitive(self, browser):
        add_file = AddFile(object, object)
        add_file.allowed_extensions = ['.my_extension']

        file_lower = DummyFile('james.my_extension')
        file_upper = DummyFile('james.MY_EXTENSION')

        self.assertFalse(add_file.is_wrong_type(file_lower))
        self.assertFalse(add_file.is_wrong_type(file_upper))
