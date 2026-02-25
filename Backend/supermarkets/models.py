from django.db import models

# Create your models here.

from django.db import models


class Supermarket(models.Model):

    name = models.CharField(max_length=255)

    location = models.CharField(max_length=255)

    region = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
