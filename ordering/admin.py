from django.contrib import admin

from .models import Order, Product, Profile, Store, Category, StoreCategoryProduct, OrderProduct

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(StoreCategoryProduct)
admin.site.register(OrderProduct)
