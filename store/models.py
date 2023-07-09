from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='products', null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self) -> str:
        return self.user.username

class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    orderdate = models.DateField(default=date.today)
    isdelivered = models.BooleanField(default=False)
    isoutfordelivery = models.BooleanField(default=False)
    isshipped = models.BooleanField(default=False)
    isordered = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.pk}"

