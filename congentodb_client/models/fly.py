from django.db import models
from model_utils import Choices


class Fly(models.Model):

    ORIGINS = Choices(
        ("center", "Stock Center"),
        ("internal", "Internal Lab"),
        ("external", "External Lab"),
    )

    created = models.DateTimeField("Created", auto_now_add=True)
    modified = models.DateTimeField("Updated", auto_now=True)
    categories = models.TextField("Category", blank=True)
    species = models.CharField("Species", max_length=80)
    origin = models.CharField(max_length=8, choices=ORIGINS, default=ORIGINS.center)
    origin_center = models.CharField("Stock center", max_length=100, blank=True)
    genotype = models.CharField("Genotype", max_length=255, blank=True)

    chrx = models.CharField(max_length=60, verbose_name="Chromosome X", blank=True)
    chry = models.CharField(max_length=60, verbose_name="Chromosome Y", blank=True)
    chr2 = models.CharField(max_length=60, verbose_name="Chromosome 2", blank=True)
    chr3 = models.CharField(max_length=60, verbose_name="Chromosome 3", blank=True)
    chr4 = models.CharField(max_length=60, verbose_name="Chromosome 4", blank=True)
    bal1 = models.CharField(max_length=60, verbose_name="Balancer 1", blank=True)
    bal2 = models.CharField(max_length=60, verbose_name="Balancer 2", blank=True)
    bal3 = models.CharField(max_length=60, verbose_name="Balancer 3", blank=True)
    chru = models.CharField(max_length=60, verbose_name="Unknown genotype", blank=True)

    special_husbandry_conditions = models.TextField(blank=True)
    line_description = models.TextField(blank=True)

    remote_id = models.BigIntegerField("Remote ID")

    class Meta:
        verbose_name = "Fly"
        verbose_name_plural = "Flies"

    class APIMeta:
        db_name = "api"
        resource_path = "fly"
        resource_name_plural = "flies"
