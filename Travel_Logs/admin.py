from django.contrib import admin

# Register your models here.
from Travel_Logs.models import Location, Entry
admin.site.register(Location)
admin.site.register(Entry)