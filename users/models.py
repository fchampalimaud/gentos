import logging

from django.apps import apps
from django.conf import settings

# from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices


logger = logging.getLogger(__name__)


def get_installed_dbs():
    for app_label in ("fishdb", "flydb", "rodentdb"):
        try:
            app_config = apps.get_app_config(app_label)
        except LookupError:
            logger.warning("Could not find app_config for '%s'", app_label)
        else:
            yield (app_config.label, app_config.verbose_name)


# class User(AbstractUser):
#     ...


class Institution(models.Model):
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(
        upload_to="institution", blank=True, help_text="recommended size 220x40 px"
    )

    def __str__(self):
        return self.name


class DatabaseAccess(models.Model):
    ACCESS_LEVELS = Choices(
        ("admin", "Group members can manage all entries"),
        ("basic", "Group members can only manage their own entries"),
        ("view", "Group members can only view"),
    )

    group = models.ForeignKey(
        to="users.Group", on_delete=models.CASCADE, related_name="accesses"
    )
    db = models.CharField(
        verbose_name="database", max_length=10, choices=get_installed_dbs()
    )
    level = models.CharField(
        verbose_name="access level",
        max_length=6,
        choices=ACCESS_LEVELS,
        default=ACCESS_LEVELS.view,
    )

    class Meta:
        verbose_name = "database access"
        verbose_name_plural = "database accesses"
        unique_together = ("group", "db")


class Group(models.Model):
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    institution = models.ForeignKey(to="Institution", on_delete=models.CASCADE)
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through="Membership")

    def __str__(self):
        return self.name

    def clean(self):
        if not self.pk:
            # avoids ValueError:
            # needs to have a value for field "id" before this
            # many-to-many relationship can be used
            return

        responsible_found = False
        for user in self.users.all():
            print(user)
            print(user.__dict__)
            # if user

        # TODO
        # FIXME


class Membership(models.Model):
    user = models.ForeignKey(
        to="auth.User", on_delete=models.CASCADE, related_name="memberships"
    )
    group = models.ForeignKey(
        to="Group", on_delete=models.CASCADE, related_name="memberships"
    )

    is_responsible = models.BooleanField(
        verbose_name="responsible",
        default=False,
        help_text="Designates whether the user is the POC.",
    )
    is_manager = models.BooleanField(
        verbose_name="manager",
        default=False,
        help_text=(
            "Designates whether the user has permissions to manage all group "
            "entries in the database."
        ),
    )

    def __str__(self):
        return f"{self.user.get_short_name()} is a member of {self.group}"