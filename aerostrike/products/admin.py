from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'is_approved')
    list_filter = ('product_type', 'is_approved')
    search_fields = ('name',)
