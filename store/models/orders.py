from datetime import datetime
from tkinter import CASCADE
from django.db import models
from .product import Product
from .customer import Customer
import datetime

class orders(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    Phone = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
    paymentdetails = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=50)
    razorpay_payment_id = models.CharField(max_length=50)
    status_choice = (
    ("pending" , "PENDING"),
    ('Order Placed','ORDER PLACED'),
    ('Shiped','SHIPED'),
    ('Out for delivery','OUT FOR DELIVERY'),
    ('Delivered','DELIVERED'),
    ('Failed','FAILED'),
)
    status = models.CharField(choices=status_choice,max_length=20)



    def place_order(self):
        self.save()

    @staticmethod
    def get_customer_by_id(customer_id):
        return orders.objects.filter(customer = customer_id).order_by('-time')

    def get_customer_by_orderid(orderid):
        return orders.objects.filter(razorpay_order_id = orderid)