from django.contrib import admin

from . import models


@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
    ...


class MembershipInline(admin.TabularInline):
    model = models.Membership


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "group", "is_responsible", "is_manager"]
    list_filter = ["group", "is_responsible", "is_manager"]
