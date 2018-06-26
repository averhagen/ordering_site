from django.contrib import admin

from .models import Order, Product, User, Store, StoreMenuOption

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Store)
admin.site.register(StoreMenuOption)
