from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='products/')
    content = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    creation_time = models.DateTimeField(auto_now_add=True)
    confirmation_time = models.DateTimeField(null=True, blank=True)

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    payment_type = models.CharField(max_length=20)