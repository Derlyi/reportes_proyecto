from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'discount',  # Agregar descuento a la lista de visualización
        'quantity',  # Agregar cantidad a la lista de visualización
        'available',
    ]
    list_filter = ['available']
    list_editable = ['price', 'available', 'discount', 'quantity']  # Hacer editable el descuento y la cantidad
    prepopulated_fields = {'slug': ('name',)}
