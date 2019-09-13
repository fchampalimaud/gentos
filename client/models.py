from django.db import models

from fishdb.base_fish import AbstractFish
from fishdb.models.category import AbstractCategory
from fishdb.models.species import AbstractSpecies


class CongentoRecord(models.Model):
    congento_id = models.PositiveIntegerField("Remote ID")

    class Meta:
        abstract = True


class Fish(CongentoRecord, AbstractFish):

    class APIMeta:
        db_name = 'api'
        resource_path = 'fish'
        resource_name = 'fish'
        resource_name_plural = 'fish'

    # Redirect foreign keys to the Models defined here
    category = models.ForeignKey(
        to="Category", on_delete=models.PROTECT, related_name="fish"
    )
    species = models.ForeignKey(
        to="Species", on_delete=models.PROTECT, related_name="fish"
    )


class Category(AbstractCategory):

    class APIMeta:

        db_name = 'api'
        resource_path = 'fish-categories'
        resource_name = 'category'
        resource_name_plural = 'categories'


class Species(AbstractSpecies):

    class APIMeta:
        db_name = 'api'
        resource_path = 'fish-species'
        resource_name = 'species'
        resource_name_plural = 'species'
