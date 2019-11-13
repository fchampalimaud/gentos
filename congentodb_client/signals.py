import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.db.utils import ConnectionDoesNotExist
from django.dispatch import receiver

from congentodb_client.models import Fish as RemoteFish
from congentodb_client.models import Fly as RemoteFly
from congentodb_client.models import Rodent as RemoteRodent
from congentodb_client.models import MissedSync

from fishdb.models import Fish
from flydb.models import Fly
from rodentdb.models import Rodent

logger = logging.getLogger(__name__)


# =============================================================================
# RODENT
# =============================================================================


@receiver(post_save, sender=Rodent)
def save_remote_rodent(sender, instance, created, **kwargs):

    if not created and not instance.public:
        # When an object becomes private remove it from the remote database
        try:
            remote_obj = RemoteRodent.objects.get(remote_id=instance.pk)
            remote_obj.delete()
        except RemoteRodent.DoesNotExist:
            pass
        except ConnectionDoesNotExist:
            logger.debug("Could not connect to Congento API")
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Rodent),
                object_id=instance.pk,
                operation="D",
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

        except ConnectionDoesNotExist:
            logger.debug("Could not connect to Congento API")
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Rodent),
                object_id=instance.pk,
                operation="U",
            ).save()
            print(e)


@receiver(post_delete, sender=Rodent)
def delete_remote_rodent(sender, instance, **kwargs):

    try:
        remote_obj = RemoteRodent.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except RemoteRodent.DoesNotExist:
        pass
    except ConnectionDoesNotExist:
        logger.debug("Could not connect to Congento API")
    except Exception as e:
        MissedSync(
            contenttype=ContentType.objects.get_for_model(Rodent),
            object_id=instance.pk,
            operation="D",
        ).save()
        print(e)


# =============================================================================
# FLY
# =============================================================================


@receiver(post_save, sender=Fly)
def save_remote_fly(sender, instance, created, **kwargs):

    if not created and not instance.public:
        # When an object becomes private remove it from the remote database
        try:
            remote_obj = RemoteFly.objects.get(remote_id=instance.pk)
            remote_obj.delete()
        except RemoteFly.DoesNotExist:
            pass
        except ConnectionDoesNotExist:
            logger.debug("Could not connect to Congento API")
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Fly),
                object_id=instance.pk,
                operation="D",
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
            remote_obj.special_husbandry_conditions = (
                instance.special_husbandry_conditions
            )
            remote_obj.line_description = instance.line_description

            remote_obj.save()
        except ConnectionDoesNotExist:
            logger.debug("Could not connect to Congento API")
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Fly),
                object_id=instance.pk,
                operation="U",
            ).save()
            print(e)


@receiver(post_delete, sender=Fly)
def delete_remote_fly(sender, instance, **kwargs):

    try:
        remote_obj = RemoteFly.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except RemoteFly.DoesNotExist:
        pass
    except ConnectionDoesNotExist:
        logger.debug("Could not connect to Congento API")
    except Exception as e:
        MissedSync(
            contenttype=ContentType.objects.get_for_model(Fly),
            object_id=instance.pk,
            operation="D",
        ).save()
        print(e)


# =============================================================================
# FISH
# =============================================================================


@receiver(post_save, sender=Fish)
def save_remote_Fish(sender, instance, created, **kwargs):

    if not created and not instance.public:
        # When an object becomes private remove it from the remote database
        try:
            remote_obj = RemoteFish.objects.get(remote_id=instance.pk)
            remote_obj.delete()
        except RemoteFish.DoesNotExist:
            pass
        except ConnectionDoesNotExist:
            logger.debug("Could not connect to Congento API")
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Fish),
                object_id=instance.pk,
                operation="D",
            ).save()
            print(e)

    elif instance.public:

        try:
            try:
                remote_obj = RemoteFish.objects.get(remote_id=instance.pk)
            except RemoteFish.DoesNotExist:
                remote_obj = RemoteFish(remote_id=instance.pk)

            remote_obj.availability = instance.availability
            remote_obj.link = instance.link
            remote_obj.strain_name = instance.strain_name
            remote_obj.common_name = instance.common_name
            remote_obj.background = instance.background
            remote_obj.genotype = instance.genotype
            remote_obj.phenotype = instance.phenotype
            remote_obj.origin = instance.origin
            remote_obj.quarantine = instance.quarantine
            remote_obj.mta = instance.mta
            remote_obj.line_description = instance.line_description
            remote_obj.category_name = instance.category.name if instance.category else ""
            remote_obj.species_name = instance.species.name if instance.species else ""

            remote_obj.save()
        except ConnectionDoesNotExist:
            logger.debug("Could not connect to Congento API")
        except Exception as e:
            MissedSync(
                contenttype=ContentType.objects.get_for_model(Fish),
                object_id=instance.pk,
                operation="U",
            ).save()
            print(e)


@receiver(post_delete, sender=Fish)
def delete_remote_Fish(sender, instance, **kwargs):

    try:
        remote_obj = Fish.objects.get(remote_id=instance.pk)
        remote_obj.delete()
    except Fish.DoesNotExist:
        pass
    except:
        MissedSync(
            contenttype=ContentType.objects.get_for_model(Fish),
            object_id=instance.pk,
            operation="D",
        ).save()
