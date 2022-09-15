from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import View
import random
from django.core.mail import send_mail
from eshop import settings

def generateotp():
     generateotp.Actualotp = random.randint(1000, 9999)
     return generateotp.Actualotp

def sendotp(request):
    if request.method=='POST':
        generateotp() 
        email = request.session['email']
        print(email)
        send_mail('E-Shop OTP Verification', 'Your otp for email verification is '+str(generateotp.Actualotp)+' please dont share your otp',settings.EMAIL_HOST_USER,
                      [email], fail_silently=False)
        print(generateotp.Actualotp)  
        return render (request,'validotp.html')  

def getemail(request):
    if request.method == 'GET': 
        return render (request,'getemail.html')
    if request.method == 'POST': 
        email = request.POST.get('email')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            request.session['email'] = customer.email
            generateotp()  
            sendotp(request)
            return render (request,'validotp.html') 
        else:
            error_message = 'incorect email address'   
        return render(request,'getemail.html',{'error_message':error_message})

def validateotp(request):
    if request.method == 'GET':
        return render (request,'validotp.html')
    else:
        error_message = None
        otp = request.POST.get('otp')
        if otp == '' or str:
            error_message = 'invalid otp'
            return render (request,'validotp.html',{'error_message':error_message})
        elif generateotp.Actualotp == int(otp):
            return redirect('homepage')    
        else:
            error_message = 'invalid otp'
            return render (request,'validotp.html',{'error_message':error_message})
