from django.db import models


class UserQuerySet(models.QuerySet):
    def fishdb_users(self):
        return self.filter(memberships__group__accesses__animaldb="fishdb")

    def flydb_users(self):
        return self.filter(memberships__group__accesses__animaldb="flydb")

    def rodentdb_users(self):
        return self.filter(memberships__group__accesses__animaldb="rodentdb")
