from zope.component import getUtility
from zope.i18n import ITranslationDomain
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('ftw.events')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    update_plone_translation_order()


def update_plone_translation_order():
    """By moving the plone.app.locales translations to the bottom of the list of
    translation catalogs we can make sure translations customizations actually
    take effect.
    This makes ZCML load order irrelevant.
    """
    translation_domain = getUtility(ITranslationDomain, name='plone')
    for _language, catalogs in translation_domain.getCatalogsInfo().items():
        for path in filter(lambda path: 'plone.app.locales' in path, catalogs):
            # move to bottom
            catalogs.remove(path)
            catalogs.append(path)
