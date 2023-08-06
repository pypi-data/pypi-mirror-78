from ftw.events.utils import IS_PLONE_5
from ftw.upgrade import UpgradeStep


class DefineScaleForEventsListingImage(UpgradeStep):
    """Define scale for event listing image.
    """

    def __call__(self):
        if IS_PLONE_5:
            self.install_upgrade_profile(['plone.app.registry'])
        else:
            self.install_upgrade_profile(['propertiestool'])
