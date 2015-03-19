from ftw.upgrade import UpgradeStep


class PermissionsForSiteAdministrator(UpgradeStep):
    """Extend permissions for Site Administrator (same as Manager).
    """

    def __call__(self):
        self.setup_install_profile(
            'profile-ftw.billboard.upgrades:1222'
        )

        self.update_workflow_security(
            ['ftw_billboard_ad_workflow', 'ftw_billboard_category_workflow'],
            reindex_security=True
        )
