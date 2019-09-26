from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import forms as auth_forms

from . import models


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):

    form = auth_forms.UserChangeForm
    add_form = auth_forms.UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "email", "is_superuser"]
    search_fields = ["name", "email"]


class DatabaseInline(admin.TabularInline):
    model = models.DatabaseAccess
    extra = 0


class MembershipInline(admin.TabularInline):
    model = models.Membership
    extra = 0


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [DatabaseInline, MembershipInline]


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "group", "is_responsible", "is_manager"]
    list_filter = ["group", "is_responsible", "is_manager"]
