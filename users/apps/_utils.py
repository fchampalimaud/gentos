"""
Utilities shared by all animal models apps.
"""

from pyforms_web.web.middleware import PyFormsMiddleware


class FormPermissionsMixin:
    def get_readonly(self, default):
        user = PyFormsMiddleware.user()
        animaldb = self.model._meta.app_label
        access_level = user.get_access_level(animaldb)

        default = ["created", "modified"]

        if access_level in ("superuser", "admin"):
            pass
        elif access_level in ("manager",) and self._object_belongs_to_user_group():
            default += ["ownership"]
        else:
            default += ["maintainer", "ownership"]

        return default

    def update_object_fields(self, obj):
        obj = super().update_object_fields(obj)

        if obj._state.adding:
            user = PyFormsMiddleware.user()
            access_level = user.get_access_level(self.model._meta.app_label)

            if access_level in ("manager", "basic"):
                obj.ownership = user.get_group()

            if access_level == "basic":
                obj.maintainer = user

        return obj

    def _object_belongs_to_user_group(self):
        """
        Returns True if the object being edited using the form belongs
        to the current user.
        """
        if self.model_object:
            user = PyFormsMiddleware.user()
            return self.model_object.ownership == user.get_group()
        return False


def limit_choices_to_database(animaldb, field, queryset):
    """Limit the query for related fields to values related with a DB."""
    user = PyFormsMiddleware.user()

    if field.name == "maintainer":
        queryset = queryset.filter(group__accesses__animaldb=animaldb)
        if user.is_manager():
            queryset = queryset.filter(group=user.get_group())

    if field.name == "ownership":
        queryset = queryset.filter(accesses__animaldb=animaldb)

    return queryset.distinct()
