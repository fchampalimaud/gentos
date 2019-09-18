import traceback

from django.contrib.contenttypes.models import ContentType
from rodentdb.models import Rodent
#from fishdb.models import Zebrafish
from flydb.models import Fly
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from congentodb_client.models.rodent import Rodent as RemoteRodent
from congentodb_client.models.fly import Fly as RemoteFly
from congentodb_client.models.fish import Fish as RemoteFish
from congentodb_client.models.missed_sync import MissedSync

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
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Rodent),
                object_id=instance.pk,
                operation='D'
            ).save()
            print(e)

    elif instance.public:

        try:
            try:
                remote_obj = RemoteRodent.objects.get(remote_id=instance.pk)
            except RemoteRodent.DoesNotExist:
                remote_obj = RemoteRodent(remote_id=instance.pk)

            remote_obj.availability = instance.availability
            remote_obj.link = instance.link
            remote_obj.species = instance.species.name if instance.species else None

            remote_obj.strain_name = instance.strain_name
            remote_obj.common_name = instance.common_name
            remote_obj.origin = instance.origin.name if instance.origin else None
            remote_obj.origin_other = instance.origin_other
            remote_obj.category = instance.category.name if instance.category else None
            remote_obj.background = instance.background.name if instance.background else None
            remote_obj.zygosity = instance.zygosity.name if instance.zygosity else None

            remote_obj.line_description = instance.line_description
            remote_obj.coat_color = instance.coat_color.name if instance.coat_color else None
            remote_obj.reporter_gene = instance.reporter_gene.name if instance.reporter_gene else None
            remote_obj.inducible_cassette = instance.inducible_cassette.name if instance.inducible_cassette else None

            remote_obj.save()

        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Rodent),
                object_id=instance.pk,
                operation='U'
            ).save()
            print(e)
            #traceback.print_stack()





@receiver(post_delete, sender=Rodent)
def delete_remote_rodent(sender, instance, **kwargs):

    try:
        remote_obj = RemoteRodent.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except RemoteRodent.DoesNotExist:
        pass
    except Exception as e:
        MissedSync(
            contenttype=ContentType.objects.get_for_model(Rodent),
            object_id=instance.pk,
            operation='D'
        ).save()
        print(e)


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
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Fly),
                object_id=instance.pk,
                operation='D'
            ).save()
            print(e)


    elif instance.public:

        try:
            try:
                remote_obj = RemoteFly.objects.get(remote_id=instance.pk)
            except RemoteFly.DoesNotExist:
                remote_obj = RemoteFly(remote_id=instance.pk)

            remote_obj.categories = "; ".join([x.name for x in instance.categories.all()])
            remote_obj.species = instance.species.specie_name if instance.species else None
            remote_obj.origin = instance.origin
            remote_obj.origin_center = instance.origin_center
            remote_obj.genotype = instance.genotype

            remote_obj.chrx = instance.chrx
            remote_obj.chry = instance.chry
            remote_obj.bal1 = instance.bal1
            remote_obj.chr2 = instance.chr2
            remote_obj.bal2 = instance.bal2
            remote_obj.chr3 = instance.chr3
            remote_obj.bal3 = instance.bal3
            remote_obj.chr4 = instance.chr4
            remote_obj.chru = instance.chru
            remote_obj.special_husbandry_conditions = instance.special_husbandry_conditions
            remote_obj.line_description = instance.line_description

            remote_obj.save()
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Fly),
                object_id=instance.pk,
                operation='U'
            ).save()
            print(e)


@receiver(post_delete, sender=Fly)
def delete_remote_fly(sender, instance, **kwargs):

    try:
        remote_obj = RemoteFly.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except RemoteFly.DoesNotExist:
        pass
    except Exception as e:
        MissedSync(
            contenttype=ContentType.objects.get_for_model(Fly),
            object_id=instance.pk,
            operation='D'
        ).save()
        print(e)




####################################################
### ZEBRAFISH ######################################
####################################################
"""
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
        except:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Zebrafish),
                object_id=instance.pk,
                operation='D'
            ).save()

    elif instance.public:

        try:
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
        except:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Zebrafish),
                object_id=instance.pk,
                operation='U'
            ).save()




@receiver(post_delete, sender=Zebrafish)
def delete_remote_zebrafish(sender, instance, **kwargs):

    try:
        remote_obj = Zebrafish.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except Zebrafish.DoesNotExist:
        pass
    except:
        MissedSync(
            contenttype=ContentType.objects.get_for_model(Zebrafish),
            object_id=instance.pk,
            operation='D'
        ).save()
"""
