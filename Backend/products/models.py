from django.db import models
from supermarkets.models import Supermarket


class Category(models.Model):
    supermarket = models.ForeignKey(
        Supermarket,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.supermarket.name}"


class Product(models.Model):
    supermarket = models.ForeignKey(
        Supermarket,
        on_delete=models.CASCADE,
        related_name="products"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    # Replaced URLField with ImageField for real file uploads
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.supermarket.name}"

    @property
    def image_url(self):
        """Returns full image URL or empty string — keeps frontend compatible."""
        if self.image:
            return self.image.url
        return ""