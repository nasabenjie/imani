from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "supermarket", "created_at")
    list_filter = ("supermarket",)
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "supermarket", "price", "stock", "created_at")

    list_filter = ("supermarket",)

    search_fields = ("name",)