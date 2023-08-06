from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import IS_PLONE_5
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig


class ServicenavigationLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER, )

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '  <include package="plone.app.relationfield" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'ftw.servicenavigation')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.servicenavigation:default')
        if IS_PLONE_5:
            applyProfile(portal, 'plone.app.contenttypes:default')

    def tearDownZope(self, app):
        super(ServicenavigationLayer, self).tearDownZope(app)


SERVICENAVIGATION_FIXTURE = ServicenavigationLayer()
SERVICENAVIGATION_FUNCTIONAL = FunctionalTesting(
    bases=(
        SERVICENAVIGATION_FIXTURE,
        set_builder_session_factory(functional_session_factory),
    ),
    name='ftw.servicenavigation:functional',
)
