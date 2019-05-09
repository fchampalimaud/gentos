from rodentdb.models import Rodent
from fishdb.models import Zebrafish
from flydb.models import Fly
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from congentodb_client.models.rodent import Rodent as RemoteRodent
from congentodb_client.models.fly import Fly as RemoteFly
from congentodb_client.models.zebrafish import Zebrafish as RemoteZebrafish
from django.contrib.auth.models import User

####################################################
### RODENT #########################################
####################################################

@receiver(post_save, sender=Rodent)
def save_remote_rodent(sender, instance, created, **kwargs):

    if not created and not instance.public:

        # for the case an object becomes private
        # remove it from the remote database
        try:
            remote_obj = RemoteRodent.objects.get(remote_id=instance.pk)
            remote_obj.delete()
        except RemoteRodent.DoesNotExist:
            pass

    elif instance.public:

        try:
            remote_obj = RemoteRodent.objects.get(remote_id=instance.pk)
        except RemoteRodent.DoesNotExist:
            remote_obj = RemoteRodent(remote_id=instance.pk)

        remote_obj.species = instance.species
        remote_obj.strain_name = instance.strain_name
        remote_obj.common_name = instance.common_name
        remote_obj.origin = instance.origin
        remote_obj.availability = instance.availability
        remote_obj.comments = instance.comments
        remote_obj.link = instance.link
        remote_obj.mta = instance.mta
        remote_obj.background = instance.background
        remote_obj.background_other = instance.background_other
        remote_obj.genotype = instance.genotype
        remote_obj.genotype_other = instance.genotype_other
        remote_obj.model_type = instance.model_type
        remote_obj.model_type_other = instance.model_type_other
        remote_obj.save()




@receiver(post_delete, sender=Rodent)
def delete_remote_rodent(sender, instance, **kwargs):

    try:
        remote_obj = RemoteRodent.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except RemoteRodent.DoesNotExist:
        pass




####################################################
### FLY ############################################
####################################################

@receiver(post_save, sender=Fly)
def save_remote_fly(sender, instance, created, **kwargs):

    if not created and not instance.public:

        # for the case an object becomes private
        # remove it from the remote database
        try:
            remote_obj = RemoteFly.objects.get(remote_id=instance.pk)
            remote_obj.delete()
        except RemoteFly.DoesNotExist:
            pass

    elif instance.public:

        try:
            remote_obj = RemoteFly.objects.get(remote_id=instance.pk)
        except RemoteFly.DoesNotExist:
            remote_obj = RemoteFly(remote_id=instance.pk)

        remote_obj.chrx = instance.chrx
        remote_obj.chry = instance.chry
        remote_obj.bal1 = instance.bal1
        remote_obj.chr2 = instance.chr2
        remote_obj.bal2 = instance.bal2
        remote_obj.chr3 = instance.chr3
        remote_obj.bal3 = instance.bal3
        remote_obj.chr4 = instance.chr4
        remote_obj.chru = instance.chru
        remote_obj.legacy1 = instance.legacy1
        remote_obj.legacy2 = instance.legacy2
        remote_obj.legacy3 = instance.legacy3
        remote_obj.flydbid = instance.flydbid
        remote_obj.hospital = instance.hospital
        remote_obj.died = instance.died
        remote_obj.genotype = instance.genotype
        remote_obj.category = instance.category
        remote_obj.specie = instance.specie
        remote_obj.save()


@receiver(post_delete, sender=Fly)
def delete_remote_fly(sender, instance, **kwargs):

    try:
        remote_obj = RemoteFly.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except RemoteFly.DoesNotExist:
        pass




####################################################
### ZEBRAFISH ######################################
####################################################

@receiver(post_save, sender=Zebrafish)
def save_remote_zebrafish(sender, instance, created, **kwargs):

    if not created and not instance.public:

        # for the case an object becomes private
        # remove it from the remote database
        try:
            remote_obj = RemoteZebrafish.objects.get(remote_id=instance.pk)
            remote_obj.delete()
        except RemoteZebrafish.DoesNotExist:
            pass

    elif instance.public:

        try:
            remote_obj = RemoteZebrafish.objects.get(remote_id=instance.pk)
        except RemoteZebrafish.DoesNotExist:
            remote_obj = RemoteZebrafish(remote_id=instance.pk)

        remote_obj.background = instance.background
        remote_obj.genotype = instance.genotype
        remote_obj.phenotype = instance.phenotype
        remote_obj.origin = instance.origin
        remote_obj.availability = instance.availability
        remote_obj.comments = instance.comments
        remote_obj.link = instance.link
        remote_obj.mta = instance.mta

        remote_obj.line_name = instance.line_name
        remote_obj.line_number = instance.line_number
        remote_obj.line_type = instance.line_type
        remote_obj.line_type_other = instance.line_type_other
        remote_obj.save()

@receiver(post_delete, sender=Zebrafish)
def delete_remote_zebrafish(sender, instance, **kwargs):

    try:
        remote_obj = RemoteZebrafish.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except RemoteZebrafish.DoesNotExist:
        pass




# set a new user inactive by default
@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance.pk is None and not instance.is_superuser:
        instance.is_active = False
