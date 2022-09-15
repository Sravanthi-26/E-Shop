from itertools import product
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Product


class Cart(View):
    def get(self,request): 
        cart = request.session.get('cart')
        if cart:
            ids = list(request.session.get('cart').keys())
            products = Product.get_products_by_id(ids)
            return render (request,'cart.html',{'products':products})
        else:
            return render (request,'emptycart.html')