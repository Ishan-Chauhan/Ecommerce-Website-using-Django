from django.contrib import admin
from .models import Category, Product, Cart
from .models import Status

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Status)