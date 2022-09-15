from itertools import product
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import View
from store.models.orders import orders


class OrdersView(View):
    def get(self,request): 
        customer = request.session.get('customer_id')
        order = orders.get_customer_by_id(customer)
        print(customer,order)
        return render (request,'orders.html',{'order':order})