from asyncio import streams
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View
from django.core.mail import send_mail
from eshop import settings
import random
def generateotp():
     generateotp.Actualotp = random.randint(1000, 9999)
     return generateotp.Actualotp

def passwordresetotp(request):
    if request.method=='POST':
        generateotp() 
        email = request.session['email']
        print(email)
        send_mail('E-Shop Password reset OTP', 'Your otp for password reset is '+str(generateotp.Actualotp)+' please dont share your otp',settings.EMAIL_HOST_USER,
                      [email], fail_silently=False)
        print(generateotp.Actualotp)  
        return render (request,'validotp.html')  
        
def password_reset_request(request):
    if request.method == 'GET':
        return render (request,'password_reset.html')
    else: 
        email = request.POST.get('email')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            request.session['email'] = customer.email
            generateotp()  
            passwordresetotp(request)
            return render (request,'password_reset_confirm.html') 
        else:
            error_message = 'incorect email address'   
        return render(request,'password_reset.html',{'error_message':error_message})

def password_reset_form(request):
    if request.method == 'GET':
        return render (request,'password_reset_confirm.html')
    else: 
        password1 = request.POST.get('ps1')
        password2 = request.POST.get('ps2')
        otp = request.POST.get('otp')
        error_message = None
        if otp == '' or str:
            error_message = 'invalid otp'
            return render (request,'password_reset_confirm.html',{'error_message':error_message})
        if generateotp.Actualotp == int(otp):
            if password1 == password2:
                email = request.session['email']
                hashpassword = make_password(password1)
                Customer.objects.filter(email = email).update(password = hashpassword)
                return render (request,'password_reset_complete.html') 
            else:
                error_message = 'password and confirm password does not match'   
                return render(request,'password_reset_confirm.html',{'error_message':error_message}) 
        else:
            error_message = 'incorrect otp'   
            return render(request,'password_reset_confirm.html',{'error_message':error_message})        
