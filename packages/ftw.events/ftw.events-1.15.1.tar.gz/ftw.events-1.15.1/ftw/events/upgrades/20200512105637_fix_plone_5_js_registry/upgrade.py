from ftw.upgrade import UpgradeStep
import pkg_resources


IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'


class FixPlone5JsRegistry(UpgradeStep):
    """Fix plone 5 js registry.
    """

    def __call__(self):
        if IS_PLONE_5:
            # Add bundle for ftw.events
            self.install_upgrade_profile()
            # Fix resource of ftw.keywordwidget
            self.setup_install_profile(
                'profile-ftw.keywordwidget:default',
                steps=['plone.app.registry'])
