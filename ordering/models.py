from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name        

class Order(models.Model):
    date_ordered = models.DateTimeField('date ordered')

    def __str__(self):
        return id + " " + self.date_ordered


class User(models.Model):
    email = models.EmailField(unique = True)

    def __str__(self):
        return self.email
