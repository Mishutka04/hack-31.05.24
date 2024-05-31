from django.contrib import admin
from .models import Region, Subdivision, Vehicle #, Trip, Telematics

admin.site.register(Region)
admin.site.register(Subdivision)
admin.site.register(Vehicle)
# admin.site.register(Trip)
# admin.site.register(Telematics)