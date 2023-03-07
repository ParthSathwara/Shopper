from django.contrib import admin
from .models import *


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']

@admin.register(PlacedOrder)
class PlacedOrderModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer', 'product', 'quantity', 'orered_date', 'status']