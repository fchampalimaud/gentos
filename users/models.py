import logging

from django.apps import apps
from django.conf import settings

from django.contrib.auth.models import AbstractUser
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


class User(AbstractUser):

    def __str__(self):
        return self.get_full_name() or f"{self.username} <{self.email}>"

    def get_group(self):
        # FIXME what if user has access through multiple groups?
        memberships = self.memberships.all()
        group = self.memberships.first().group
        return group

    def get_access_level(self, animaldb):
        """
        animaldb: one of 'fishdb', 'flydb', 'rodentdb'

        Returns the access level this user has to the database:
            - 'admin', 'manager', 'basic', 'view', None
        """

        if self.is_superuser:
            return "superuser"

        can_access_db = self.memberships.filter(
            group__accesses__animaldb=animaldb,
        ).exists()

        if can_access_db:
            if self.memberships.filter(is_manager=True).exists():
                return "manager"
            if self.memberships.filter(group__accesses__animaldb=animaldb, group__accesses__level="admin").exists():
                return "admin"
            if self.memberships.filter(group__accesses__animaldb=animaldb, group__accesses__level="basic").exists():
                return "basic"
            if self.memberships.filter(group__accesses__animaldb=animaldb, group__accesses__level="view").exists():
                return "view"

    def is_admin(self, animaldb):
        """
        animaldb: one of 'fishdb', 'flydb', 'rodentdb'
        Returns True if user has admin access level to this database.
        """
        return self.memberships.filter(
            group__accesses__animaldb=animaldb,
            group__accesses__level="admin",
        ).exists()


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
    animaldb = models.CharField(
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
        unique_together = ("group", "animaldb")


class Group(models.Model):
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    institution = models.ForeignKey(to="users.Institution", on_delete=models.CASCADE)
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through="Membership")

    def __str__(self):
        return self.name

    def users_count(self):
        return self.users.count()

    users_count.short_description = "users"

    def databases(self):
        return ", ".join([access.animaldb for access in self.accesses.all()])


class Membership(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
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
