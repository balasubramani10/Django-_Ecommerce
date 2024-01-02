from django.contrib import admin
from .models import Product, Cart,Order


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_id", "product_name", "category", "desc", "price", "image"]


class CartAdmin(admin.ModelAdmin):
    list_display = ["product_id","qty","userid"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id","userid","product_id","qty"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
