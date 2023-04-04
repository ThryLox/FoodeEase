from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category= models.ManyToManyField('Category', related_name= 'item')

    def __str__(self):
        return self.name

class Category(models.Model):
    
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OrderModel(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank =True)
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank =True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=50, blank=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f'Order:{self.created_on.strftime("%b %d %I: %M %p")}'
