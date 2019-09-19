from django.contrib import admin
from .models import Rodent, Fly, Fish, MissedSync

admin.site.register(Rodent)
admin.site.register(Fly)
admin.site.register(Fish)
admin.site.register(MissedSync)
