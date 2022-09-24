from pydoc import describe
from django.db import models

class Money(models.Model): 
    id = models.AutoField(primary_key=True)
    CHOICES = (
        ('EUR','Euro'),
        ('USD','Dollar'),
        ('MDL','Moldavian Leu'),
    )
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=4,choices=CHOICES,default='MDL')

class Product(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=300, default='')
    bar_code = models.CharField(max_length=13,default='')
    price = models.ForeignKey(Money , on_delete=models.CASCADE , null = True)

class ProductStock(models.Model):
    product =  models.ForeignKey(Product, on_delete= models.CASCADE, null = True)
    quantity = models.IntegerField()


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, default='')
    email = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15, default='')
    is_vip = models.BooleanField()
    password = models.CharField(max_length=160)

class Bag(models.Model):
    id = models.AutoField(primary_key=True)
    cost = models.ForeignKey(Money,on_delete= models.CASCADE, null = True)
    client = models.ForeignKey(Client,on_delete= models.CASCADE , null = True)

class BagItem(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product,on_delete= models.CASCADE , null = True)
    bag = models.ForeignKey(Bag,on_delete= models.CASCADE, null = True)