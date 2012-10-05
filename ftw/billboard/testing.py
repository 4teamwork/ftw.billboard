from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import z2
from zope.configuration import xmlconfig


class FtwBillboardLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.registry
        xmlconfig.file(
            'configure.zcml', plone.app.registry,
                context=configurationContext)

        import ftw.billboard

        xmlconfig.file(
            'configure.zcml', ftw.billboard,
                context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'ftw.billboard')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'plone.app.registry:default')
        applyProfile(portal, 'ftw.billboard:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_BILLBOARD_FIXTURE = FtwBillboardLayer()
FTW_BILLBOARD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_BILLBOARD_FIXTURE,), name="FtwBillboard:Integration")
