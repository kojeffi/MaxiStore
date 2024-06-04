from django.contrib import admin
from .models import Product, Order, Review, Wishlist

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Wishlist)
