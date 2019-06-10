# from django.contrib.auth.models import AbstractUser
from django.db import models


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


class Group(models.Model):
    name = models.CharField(max_length=100)
    institution = models.ForeignKey(to="Institution", on_delete=models.CASCADE)
    auth = models.ForeignKey(
        to="auth.Group", on_delete=models.CASCADE, verbose_name="authorization profile"
    )
    users = models.ManyToManyField(to="auth.User", through="Membership")

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(
        to="auth.User", on_delete=models.CASCADE, related_name="user_groups"
    )
    group = models.ForeignKey(
        to="Group", on_delete=models.CASCADE, related_name="group_members"
    )

    is_responsible = models.BooleanField("responsible", default=False)
    is_manager = models.BooleanField("manager", default=False)
