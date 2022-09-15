from django import views
from django.urls import path
from django.views.generic import RedirectView
from .views import home , signup , login 
from .views.login import logout
from .views import cart
from .views import checkout
from .views import orders
from .views import otpverification
from .views import resetpassword
from .middilewares.auth import auth_middleware , require_email
from django.contrib.auth import views as auth_view
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',home.Home.as_view(),name='homepage'),
    path('signup/',signup.Signup.as_view(),name='signuppage'),
    path('login/',login.Login.as_view(),name='loginpage'),
    path('logout/',logout,name='logout'),
    path('cart/',cart.Cart.as_view(),name='cartpage'),
    path('check-out/',auth_middleware(checkout.Checkout.as_view()),name='checkoutpage'),
    path('orders/',auth_middleware(orders.OrdersView.as_view()),name='orderspage'),
    path('sendotp/',auth_middleware(otpverification.sendotp),name='sendotp'),
    path('generateotp/',auth_middleware(otpverification.generateotp),name='generateotp'),
    path('getemail/',otpverification.getemail,name='getemail'),
    path('validateotp/',auth_middleware(otpverification.validateotp),name='validateotp'),
    path('handlerequest/',csrf_exempt(checkout.handlerequest),name='handlerequest'),
    #reset password
    path('password_reset_request/', resetpassword.password_reset_request,name='password_reset_request'),
    path('password_reset_form/', auth_middleware(resetpassword.password_reset_form),name='password_reset_form'),]
