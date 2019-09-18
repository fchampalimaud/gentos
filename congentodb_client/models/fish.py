from django.db import models
from model_utils import Choices


class Fish(models.Model):
    class APIMeta:
        db_name = "api"
        resource_path = "fish"
        resource_name = "fish"
        resource_name_plural = "fishes"

    AVAILABILITIES = Choices(
        ("live", "Live"),
        ("cryo", "Cryopreserved"),
        ("both", "Live & Cryopreserved"),
        ("none", "Unavailable"),
    )

    # Fields shared with other congento animal models
    created = models.DateTimeField("Created", auto_now_add=True)
    modified = models.DateTimeField("Updated", auto_now=True)
    availability = models.CharField(max_length=4, choices=AVAILABILITIES)
    link = models.URLField(blank=True)

    # Specific fields for this animal model
    strain_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=50, blank=True)
    background = models.CharField(max_length=30)
    genotype = models.CharField(max_length=30)
    phenotype = models.CharField(max_length=30)
    origin = models.CharField(
        verbose_name="Imported from",
        max_length=80,
        blank=True,
        help_text="Leave blank for in-house generated lines",
    )
    quarantine = models.BooleanField(verbose_name="Quarantine", default=False)
    mta = models.BooleanField(verbose_name="MTA", default=True)
    line_description = models.TextField(blank=True)

    # Foreign Keys swapped for CharFields
    category_name = models.CharField(max_length=40)
    species_name = models.CharField(max_length=80)

    remote_id = models.BigIntegerField("Remote id")
