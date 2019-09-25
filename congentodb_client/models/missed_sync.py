from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from notifications.tools import notify
from users.models import User
from flydb.models import Fly
from rodentdb.models import Rodent
from fishdb.models import Fish

from ..models import Fly as RemoteFly
from ..models import Rodent as RemoteRodent
from ..models import Fish as RemoteFish


class MissedSync(models.Model):

    OPERATIONS = (("D", "Delete"), ("U", "Update"))

    id = models.AutoField("Id", primary_key=True)  # FIXME remove

    contenttype = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name="Table"
    )
    object_id = models.IntegerField("Object id")
    operation = models.CharField("Operation", max_length=1, choices=OPERATIONS)
    committed = models.DateTimeField(
        "Committed on", null=True, blank=True, default=None
    )
    created = models.DateTimeField("Created", auto_now_add=True)
    modified = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = "Failed synchronization"
        verbose_name_plural = "Failed synchronizations"

    def __str__(self):
        return f"{self.get_operation_display()} {self.contenttype.name.title()} #{self.object_id}"

    def sync(self):
        model = self.contenttype.model_class()
        try:
            obj = model.objects.get(pk=self.object_id)

            if self.operation == "D":
                obj.delete()

            elif self.operation == "U":
                obj.save()

        except model.DoesNotExist:

            if self.operation == "D":

                if model == Fly:
                    remote_model = RemoteFly
                elif model == Rodent:
                    remote_model = RemoteRodent
                elif model == Fish:
                    remote_model = RemoteFish
                else:
                    remote_model = None

                if remote_model is not None:
                    try:
                        remote_obj = remote_model.objects.get(remote_id=self.object_id)
                    except remote_model.DoesNotExist:
                        pass
                    else:
                        remote_obj.delete()

        self.committed = timezone.now()
        self.save(send_notification=False)

    def save(self, *args, **kwargs):
        """A notification is sent to superusers on every save.
        You can override this behavior passing the argument
        `send_notification=False`.
        """
        send_notification = kwargs.pop("send_notification", True)

        super().save(*args, **kwargs)

        if send_notification:
            for user in User.objects.filter(is_superuser=True):
                notify(
                    "CONGENTODB_SYNC_ERROR",
                    "Unable to sync with the Congento DB",
                    f"Unable to sync an object from the table [{self.contenttype}].",
                    user=user,
                )
