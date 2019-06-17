from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        from .. import signals  # noqa

        from .users import UsersListApp
        from .groups import GroupsListApp

        global UsersListApp
        global GroupsListApp
