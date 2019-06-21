from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


admin.site.register(models.User, UserAdmin)


@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
    ...


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
