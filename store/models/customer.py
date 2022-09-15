import email
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime
#from django.contrib.

class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=500)
    last_login = models.DateTimeField(default=datetime.now())
    

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        else:
            return False

    @staticmethod
    def get_customer_by_email(email) :
        try:
          return Customer.objects.get(email = email) 
        except:
            return False

