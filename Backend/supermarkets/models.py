from django.db import models


class Supermarket(models.Model):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="supermarkets/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ""