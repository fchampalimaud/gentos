class PyformsPermissionsMixin:
    """Mix with models.QuerySet to manage permissions in Pyforms apps."""

    def has_add_permissions(self, user):
        access_level = user.get_access_level(self.model._meta.app_label)

        if access_level in ("superuser", "manager", "admin", "basic"):
            return True

        return False

    def has_update_permissions(self, user):
        access_level = user.get_access_level(self.model._meta.app_label)
        if access_level in ("superuser", "admin"):
            return True
        elif access_level in ("manager",):
            groups_managed_by_user = user.memberships.filter(is_manager=True).values(
                "group"
            )
            return self.filter(ownership__in=groups_managed_by_user)
        elif access_level in ("basic",):
            return self.filter(maintainer=user)
        else:
            return False

    def has_remove_permissions(self, user):
        return self.has_update_permissions(user)
