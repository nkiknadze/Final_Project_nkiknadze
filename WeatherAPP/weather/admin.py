from django.contrib import admin
from .models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'temperature', 'country', 'weather_icon', 'user']  
    search_fields = ['name', 'country']  
admin.site.register(City, CityAdmin)
