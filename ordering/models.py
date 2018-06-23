from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 200)

class Order(models.Model):
    date_ordered = models.DateTimeField('date ordered')

class User(models.Model):
    email = models.EmailField()