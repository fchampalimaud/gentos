from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from users.models import User

from flydb.models import Fly
from notifications.tools import notify
from rodentdb.models import Rodent
#from fishdb.models import Zebrafish

from ..models.fly import Fly as RemoteFly
from ..models.rodent import Rodent as RemoteRodent
from ..models.zebrafish import Zebrafish as RemoteZebrafish

class MissedSync(models.Model):

    OPERATIONS = (
      ('D', 'Delete'),
      ('U', 'Update')
    )

    id = models.AutoField('Id', primary_key=True)

    contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Table')
    object_id = models.IntegerField('Object id')
    operation  = models.CharField('Operation', max_length=1, choices=OPERATIONS )
    committed   = models.DateTimeField('Committed on', null=True, blank=True, default=None)
    created   = models.DateTimeField('Created', auto_now_add=True)
    modified  = models.DateTimeField('Updated', auto_now=True)

    def sync(self):
        model = self.contenttype.model_class()
        try:
            obj = model.objects.get(pk=self.object_id)

            if self.operation == 'D':
                obj.delete()

            elif self.operation == 'U':
                obj.save()

        except model.DoesNotExist:

            if self.operation=='D':

                remote_model = None

                if model==Fly:
                    remote_model = RemoteFly
                elif model == Rodent:
                    remote_model = RemoteRodent
                #elif model == Zebrafish:
                #    remote_model = RemoteZebrafish

                if remote_model is not None:
                    try:
                        remote_obj = remote_model.objects.get(remote_id=self.object_id)
                    except remote_model.DoesNotExist:
                        pass
                    else:
                        remote_obj.delete()

        self.committed = timezone.now()
        self.save()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for user in User.objects.filter(is_superuser=True):
            notify(
                'CONGENTODB_SYNC_ERROR',
                'Unable to sync with the Congento DB',
                f'Unable to sync an object from the table [{self.contenttype}].',
                user=user
            )