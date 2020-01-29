import logging

from allauth.account.models import EmailAddress
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.db import models
from model_utils import Choices

from .querysets import UserQuerySet

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

    name = models.CharField(verbose_name="Name", max_length=255)
    display_name = models.CharField(
        verbose_name="Display name", max_length=40, blank=True
    )

    objects = UserManager()
    db_users = UserQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def clean(self):
        super().clean()

        has_verified_email = EmailAddress.objects.filter(user=self, verified=True).exists()
        if self.is_active and not has_verified_email:
            raise ValidationError("User must verify his email first.")

        if self.is_active and not self.memberships.all().exists():
            raise ValidationError("Active users need to belong to at least one group.")

    def get_display_name(self):
        if self.display_name:
            return self.display_name
        elif self.name:
            display_name = self.name
            if len(display_name) > 40:
                display_name = display_name.split()[0]
            return display_name
        else:
            return self.username

    def get_group(self):
        # FIXME what if user has access through multiple groups?
        if self.memberships.all().exists():
            group = self.memberships.first().group
            return group
        return None

    get_group.short_description = "Group"

    def get_access_level(self, animaldb):
        """
        animaldb: one of 'fishdb', 'flydb', 'rodentdb'

        Returns the access level this user has to the database:
            - 'admin', 'manager', 'basic', 'view', None
        """

        if self.is_superuser:
            return "superuser"

        can_access_db = self.memberships.filter(
            group__accesses__animaldb=animaldb
        ).exists()

        if can_access_db:
            if self.memberships.filter(is_manager=True).exists():
                return "manager"
            if self.memberships.filter(
                group__accesses__animaldb=animaldb, group__accesses__level="admin"
            ).exists():
                return "admin"
            if self.memberships.filter(
                group__accesses__animaldb=animaldb, group__accesses__level="basic"
            ).exists():
                return "basic"
            if self.memberships.filter(
                group__accesses__animaldb=animaldb, group__accesses__level="view"
            ).exists():
                return "view"

    def is_admin(self, animaldb):
        """
        animaldb: one of 'fishdb', 'flydb', 'rodentdb'
        Returns True if user has admin access level to this database.
        """
        return self.memberships.filter(
            group__accesses__animaldb=animaldb, group__accesses__level="admin"
        ).exists()

    def is_group_manager(self, group):
        """Returns True if the user is a "manager" of the provided group."""
        return self.memberships.filter(group=group, is_manager=True).exists()

    def is_manager(self):
        """Returns True if the user is a "manager" of any group."""
        return self.memberships.filter(is_manager=True).exists()

    def is_facility_staff(self):
        """Returns True if the user has "admin" access level to any animal database."""
        return self.memberships.filter(group__accesses__level="admin").exists()


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
        verbose_name="Database", max_length=10, choices=get_installed_dbs()
    )
    level = models.CharField(
        verbose_name="Access level",
        max_length=6,
        choices=ACCESS_LEVELS,
        default=ACCESS_LEVELS.view,
    )

    class Meta:
        verbose_name = "database access"
        verbose_name_plural = "database accesses"
        unique_together = ("group", "animaldb")

    def get_label_tag(self):
        nbsp = "&nbsp" * 7  # hack to display the icon properly
        db_icons_map = {
            db[0]: f'<i class="large black congento-{db[0][:-2]} icon">{nbsp}</i>'
            for db in get_installed_dbs()
        }
        level_icons_map = {
            "admin": '<i class="grey star icon"></i>',
            "basic": '<i class="grey pencil alternate icon"></i>',
            "view": '<i class="grey eye icon"></i>',
        }
        html = (
            '<div class="ui circular label">'
            f"{db_icons_map[self.animaldb]}{level_icons_map[self.level]}"
            "</div>"
        )
        return html


class Group(models.Model):
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through="Membership")

    def __str__(self):
        return self.name

    def users_count(self):
        return self.users.count()

    users_count.short_description = "Users"

    def databases(self):
        """Lists all databases a group has access to and its access level."""
        return " ".join([f"{access.get_label_tag()}" for access in self.accesses.all()])


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
        verbose_name="Responsible",
        default=False,
        help_text="Designates whether the user is the POC.",
    )
    is_manager = models.BooleanField(
        verbose_name="Manager",
        default=False,
        help_text=(
            "Designates whether the user has permissions to manage all group "
            "entries in the database."
        ),
    )

    def __str__(self):
        return f"{self.user.get_display_name()} is a member of {self.group}"
