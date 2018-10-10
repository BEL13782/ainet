from django.contrib import admin
from .models import Client, Site, Zone, Camera, Event

# Register your models here.

admin.site.register(Client)
admin.site.register(Site)
admin.site.register(Zone)
admin.site.register(Camera)
admin.site.register(Event)