from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    weather_icon = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
