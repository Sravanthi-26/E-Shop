from unicodedata import category
from django.contrib import admin
from store.models import Product
from store.models import Category
from store.models import Customer
from store.models import orders
# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']  

class AdminCustomer(admin.ModelAdmin):
    list_display = ['firstname','email']       

admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customer,AdminCustomer)
admin.site.register(orders)


