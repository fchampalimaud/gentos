import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from rodentdb.models import Rodent
from django.contrib.auth.models import Group

"""
for i in range(1000):
    obj = Rodent()

    obj.species = "mouse"
    obj.strain_name = str(i)
    obj.common_name = str(i)
    obj.origin = str(i)
    obj.availability = 'cryo'
    obj.comments = str(i)
    obj.link = ''
    obj.mta = False
    obj.background = "sv"
    obj.background_other = ''
    obj.genotype = 'homo'
    obj.genotype_other = ''
    obj.model_type = 'ko'
    obj.model_type_other = ''
    obj.lab = Group.objects.all().first()
    obj.save()
    
"""

for obj in Rodent.objects.all():
    obj.public = True
    obj.save()