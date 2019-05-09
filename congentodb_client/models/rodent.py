from django.db import models
from model_utils import Choices

class Rodent(models.Model):

    SPECIES = Choices(
        ("rat", "Rat"),
        ("mouse", "Mouse")
    )

    BACKGROUNDS = Choices(
        ("c57bl", "C57BL/6"),
        ("balb", "Balb/c"),
        ("sv", "129sv"),
        ("fvb", "FVB"),
        ("mixed", "Mixed"),
        ("other", "Other"),
    )

    GENOTYPES = Choices(
        ("wt", "WT"),
        ("homo", "Homo"),
        ("het", "Het"),
        ("hemi", "Hemi"),
        ("both", "Homo/Het"),
        ("other", "Other"),
    )

    MODEL_TYPES = Choices(
        ("wt", "WT"),
        ("tg", "Transgenic"),
        ("ko", "KO"),
        ("cre", "Cre/flox"),
        ("other", "Other"),
    )

    # Fields shared with other congento animal models
    AVAILABILITIES = Choices(
        ("live", "Live"),
        ("cryo", "Cryopreserved"),
        ("both", "Live & Cryopreserved"),
        ("none", "Unavailable"),
    )



    created = models.DateTimeField('Created', auto_now_add=True)
    modified = models.DateTimeField('Updated', auto_now=True)
    species = models.CharField(max_length=5, choices=SPECIES)
    strain_name = models.CharField(max_length=20)
    common_name = models.CharField(max_length=20)
    origin = models.CharField(max_length=20)
    availability = models.CharField(max_length=4, choices=AVAILABILITIES)
    comments = models.TextField(blank=True)
    link = models.URLField(blank=True)
    mta = models.BooleanField(verbose_name="MTA", default=False)

    # background
    background = models.CharField(max_length=5, choices=BACKGROUNDS)
    background_other = models.CharField(max_length=20, verbose_name="Other", blank=True)

    # genotype
    genotype = models.CharField(max_length=5, choices=GENOTYPES)
    genotype_other = models.CharField(max_length=20, verbose_name="Other", blank=True)

    # model type
    model_type = models.CharField(max_length=5, choices=MODEL_TYPES)
    model_type_other = models.CharField(max_length=20, verbose_name="Other", blank=True)

    remote_id = models.BigIntegerField('Remote id')
    institution_name = models.CharField(max_length=255, blank=True, null=True)

    # the only customisation that makes this model special
    class APIMeta:
        db_name = 'api'
        resource_path = 'rodent'