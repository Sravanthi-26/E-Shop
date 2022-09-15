from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import View
from django.utils import timezone


class Login(View):
    return_url = None
    def get(self,request): 
        Login.return_url = request.GET.get('return_url')
        return render (request,'login.html')
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password') 
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password,customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['customer_email'] = customer.email
                request.session['customer_phone'] = customer.phone
                request.session['customer_name'] = customer.firstname
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
               error_message = 'email or password incorect' 
        else:
            error_message = 'email or password incorect'   
        return render(request,'login.html',{'error_message':error_message})

def logout(request):
    request.session.clear()  
    return redirect('loginpage')
