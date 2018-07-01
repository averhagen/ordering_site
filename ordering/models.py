from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 200)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    
    def __str__(self):
        return self.name        

class Order(models.Model):
    date_ordered = models.DateTimeField('date ordered')

    def __str__(self):
        return "Order #%s: %s" % (str(self.id), self.date_ordered.__str__())


class User(models.Model):
    email = models.EmailField(unique = True)

    def __str__(self):
        return self.email


class Store(models.Model):
    display_name = models.CharField(max_length = 200)
    url_identifying_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.display_name
    
    def get_menu_options_sorted_by_display_order(self):
        return self.storecategory_set.all().order_by('display_order')


class StoreCategory(models.Model):
    display_name = models.CharField(max_length = 20)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    display_order = models.IntegerField()

    def __str__(self):
        return self.display_name

    def get_products(self):
        category_products = StoreCategoryProduct.objects.filter(store_category = self.id)
        product_ids = [category_product.product.id for category_product in category_products]
        products = Product.objects.filter(id__in=product_ids)
        return products

class StoreCategoryProduct(models.Model):
    store_category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "%s : %s" % (self.store_category.__str__(), self.product.__str__())