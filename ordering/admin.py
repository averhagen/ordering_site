from django.contrib import admin

from .models import Order, Product, User, Store, StoreCategory, StoreCategoryProduct

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Store)
admin.site.register(StoreCategory)
admin.site.register(StoreCategoryProduct)
