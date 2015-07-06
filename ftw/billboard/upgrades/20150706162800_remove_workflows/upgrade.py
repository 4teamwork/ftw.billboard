from ftw.upgrade import UpgradeStep


class RemoveWorkflows(UpgradeStep):
    """Remove workflows.
    """

    def __call__(self):
        self.install_upgrade_profile()
