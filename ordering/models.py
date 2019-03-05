from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User

from colorfield.fields import ColorField

from .components import BoxSelection
import logging


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    def __str__(self):
        return self.name

    def convert_to_box_selection(self):
        price_text = "Price: %s" % self.price

        return BoxSelection(self.name, price_text, self.id) 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if(self.user is not None):
            return self.user.username
        else:
            return "hello"

    def add_product_to_cart(self, product_id) -> None:
        order_in_cart = Order.get_order_in_cart_for_user(
            self.user.id)
            
        if order_in_cart is None:
            order_in_cart = Order()
            order_in_cart.user = self.user
            order_in_cart.save()

        order_in_cart.add_product_to_order(product_id)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if(instance.profile is not None):
        instance.profile.save()


class StoreStyle(models.Model):
    DEFAULT_ID = 0
    name = models.CharField(max_length=200, default="Color Style" ,null=False)
    primary_color = ColorField(default="#FF0000", null=False)
    secondary_color = ColorField(default="#FF00FF", null=False)
    secondary_selected_color = ColorField(default="#a9a9a9", null=False)

    def __str__(self):
        return self.name

class Store(models.Model):
    display_name = models.CharField(max_length=200)
    url_identifying_name = models.CharField(max_length=20)
    style = models.ForeignKey(StoreStyle, default=StoreStyle.DEFAULT_ID, on_delete=models.SET_DEFAULT, null=False)

    def __str__(self):
        return self.display_name

    def get_categories_sorted_by_display_order(self):
        return self.category_set.all().order_by('display_order')


class Order(models.Model):
    ORDER_STATES = (
        ('IC', 'In-Cart'),
        ('OR', 'Ordered'),
        ('CM', 'Completed')
    )
    order_state = models.CharField(
        max_length=2,
        choices=ORDER_STATES,
        default='IC',
    )
    date_ordered = models.DateTimeField('date ordered', auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Order #%s: %s %s" % (str(self.id), self.user.__str__(), self.order_state)

    @staticmethod
    def find_orders_for_store_and_user(user_id, store_id):
        """Returns the orders that belong to the given store and user."""
        return Order.objects.filter(store__id=store_id).filter(user__id=user_id)

    @staticmethod
    def get_order_in_cart_for_user(user_pk) -> 'Order':
        """Returns the order that represents the users cart."""
        logging.debug('get_order_in_cart_for_user called')
        order_in_cart = Order.objects.filter(
            order_state='IC').filter(user__id=user_pk).first()
        logging.debug('order_in_cart: %s', order_in_cart)
        return order_in_cart

    def add_product_to_order(self, product_id):
        added_product = OrderProduct()
        added_product.order = self
        added_product.product = Product.objects.get(pk=product_id)
        added_product.save()


class OrderProduct(models.Model):
    """Represents an instance of a product on a particular order."""
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_products_in_cart_for_user(user_pk):
        """Returns all the products in a user's cart."""
        order_in_cart = Order.get_order_in_cart_for_user(user_pk)
        if order_in_cart is None:
            return None

        products_found_in_cart = OrderProduct.objects.filter(
            order__id=order_in_cart.id)
        logging.debug('products found in cart: %s', products_found_in_cart)
        return products_found_in_cart


class Category(models.Model):
    display_name = models.CharField(max_length=20)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    display_order = models.IntegerField()

    def __str__(self):
        return self.display_name

    @staticmethod
    def find_category_given_category_pk_and_store_pk(category_pk, store_pk):
        category = None
        if isinstance(category_pk, int):
            try:
                category = Category.objects.get(pk=category_pk)
                if category.store.id != store_pk:
                    category = None
            except Category.DoesNotExist:
                pass
        return category

    def get_products(self):
        category_products = StoreCategoryProduct.objects.filter(
            store_category=self.id)
        product_ids = [
            category_product.product.id for category_product in category_products]
        products = Product.objects.filter(id__in=product_ids)
        return products


class StoreCategoryProduct(models.Model):
    store_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "%s : %s" % (self.store_category.__str__(), self.product.__str__())
