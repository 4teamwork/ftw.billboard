from ftw.billboard import billboardMessageFactory as _
from Products.validation.i18n import recursiveTranslate
from Products.validation.i18n import safe_unicode
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements
import re


class PhoneValidator:
    """Validates a phone number."""
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        phone = re.compile('^(0|\+|00)[\d \'-/]{6,}$')
        if not phone.match(value):
            msg = _(
                "Validation failed($name: no valid phone number)",
                mapping={
                    'name': safe_unicode(self.name),
                },
            )
            return msg
        return True


class MailValidator:
    """Validates an email address."""
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        mail = re.compile("^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=" +
                          "?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?" +
                          "\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$")
        if not mail.match(value):
            msg = _(
                "Validation failed($name: no valid email)",
                mapping={
                    'name': safe_unicode(self.name),
                },
            )
            return recursiveTranslate(msg)
        return True
