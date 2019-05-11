from django.db import models

class Fly(models.Model):

    id        = models.AutoField('Id', primary_key=True)
    created   = models.DateTimeField('Created', auto_now_add=True)
    modified  = models.DateTimeField('Updated', auto_now=True)

    chrx      = models.CharField('chrX', max_length=60, blank=True, null=True)
    chry      = models.CharField('chrY', max_length=60, blank=True, null=True)
    bal1      = models.CharField('bal1', max_length=60, blank=True, null=True)
    chr2      = models.CharField('chr2', max_length=60, blank=True, null=True)
    bal2      = models.CharField('bal2', max_length=60, blank=True, null=True)
    chr3      = models.CharField('chr3', max_length=60, blank=True, null=True)
    bal3      = models.CharField('bal3', max_length=60, blank=True, null=True)
    chr4      = models.CharField('chr4', max_length=60, blank=True, null=True)
    chru      = models.CharField('chrU', max_length=60, blank=True, null=True)
    legacy1   = models.CharField('Legacy ID 1', max_length=30, blank=True, null=True)
    legacy2   = models.CharField('Legacy ID 2', max_length=30, blank=True, null=True)
    legacy3   = models.CharField('Legacy ID 3', max_length=30, blank=True, null=True)
    flydbid   = models.CharField('Fly DB ID', max_length=50, blank=True, null=True)

    genotype  = models.CharField('Genotype', max_length=255, blank=True, null=True)

    category = models.CharField('Category', max_length=255, blank=True, null=True)
    specie   = models.CharField('Specie', max_length=255,   blank=True, null=True)

    remote_id = models.BigIntegerField('Remote id')
    institution_name = models.CharField(max_length=255, blank=True, null=True)

    # the only customisation that makes this model special
    class APIMeta:
        db_name = 'api'
        resource_path = 'fly'
        resource_name_plural = 'flies'