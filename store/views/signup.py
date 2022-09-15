from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View

# Create your views here.

class Signup(View):
    def get(self , request):
       return render(request,'signup.html')
    def post(self , request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phonenumber')
        email = postData.get('email')
        password = postData.get('password')
        values = {
            'first_name' : first_name,
            'last_name' : last_name,
            'phone' : phone,
            'email' : email,
        }
        #validation
        error_message = None
        customer = Customer(firstname = first_name, lastname=last_name,phone = phone,email = email,password = password)
        error_message = self.validatacustomer(customer)
        if not error_message:
        #saving
            customer.password= make_password(customer.password)
            customer.save()
            return redirect('homepage')
        else:    
            data = {
                'error' : error_message,
                'values' : values
            }
            return render (request,'signup.html',data) 
    def validatacustomer(self,customer):
        error_message = None
        if (not customer.firstname): 
                error_message = "First Name Required !!"
        elif len(customer.firstname) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.lastname:
            error_message = 'Last Name Required'
        elif len(customer.lastname) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'email addreas alreay taken' 
        return error_message 