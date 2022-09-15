from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from store.models.product import Product
from store.models.orders import orders
from store.models.customer import Customer
from store.models.product import Product
from eshop.settings import KEY_ID,SECRET_KEY
from django.contrib.sites.shortcuts import get_current_site
import razorpay

razorpay_client = razorpay.Client(auth=(KEY_ID, SECRET_KEY))


class orderplaced(View):
    def get(self,request):
        return render (request,'orderplaced.html')

class orderfailed(View):
    def get(self,request):
        return render (request,'orderfailed.html')        

class Checkout(View):
    def get(self,request):
        return render (request,'checkout.html')
    def post(self,request):
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        customer = request.session['customer_id']
        cart = request.session.get('cart')
        cod = request.POST.get('cod')
        paymentmode = request.POST.get('paymentmode')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address,phone,customer,cart,products)
        if paymentmode == 'online':
            total_price = 0
            for p in products:
                total_price = total_price + p.price

            client = razorpay.Client(auth=(KEY_ID, SECRET_KEY))

            DATA = {
                "amount": total_price*100,
                "currency": "INR",
                "receipt": "paid",
                'payment_capture': 1
            }
            takepayment = client.order.create(data=DATA)
            Checkout.order_id = takepayment['id']
            print("orderIDDD",Checkout.order_id)
            email = request.session['customer_email']
            callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
            details = {
                'name':name , 
                'phone' : phone,
                'address' : address,
                'pincode' : pincode,
                'products' : products,
                'email' : email,
                'totalprice' : total_price,
                'key' : KEY_ID,
                'amount' : total_price * 100,
                'order' : takepayment['id'],
                'callback_url' : callback_url 
            }  
            for product in products:
                order = orders(customer = Customer(id = customer),name = name,Phone = phone , address = address , product = product, price = product.price , pincode = pincode,paymentdetails = "online payment", quantity = cart.get(str(product.id)),razorpay_order_id = Checkout.order_id , status = 'Pending')
                order.place_order()          
            return render(request,'payment.html',details)
        else:          
            for product in products:
                customer_id = request.session["customer_id"]
                orderid = "order_" + str(customer_id)
                order = orders(customer = Customer(id = customer),name = name,Phone = phone , address = address , product = product, price = product.price , pincode = pincode,paymentdetails = "Cash on Delivery", quantity = cart.get(str(product.id)),razorpay_order_id = orderid,razorpay_payment_id = "COD",status="Order PLaced")
                order.place_order()
            request.session['cart'] = {}
            return render(request,'orderplaced.html')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        order_db = orders.objects.get(razorpay_order_id=Checkout.order_id)
        try:
            order_id = request.POST.get('razorpay_order_id')
            payment_id = request.POST.get('razorpay_payment_id')
            signature = request.POST.get('razorpay_signature')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            print("order id" , order_id)
            print("payment id" , payment_id)
            print("signature" , signature)
            try:
                order_db = orders.objects.get(razorpay_order_id=order_id)
            except:                
                order_db.status = "Failed"
                order_db.save()
                request.session['cart'] = {}
                return render(request, 'orderfailed.html')
            order_db.razorpay_payment_id = payment_id
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result==None:
                order_db.status = "Failed"
                order_db.save()
                request.session['cart'] = {}
                return render(request, 'orderfailed.html')
            else:    
                    order_db.status = 'Order Placed'
                    request.session['cart'] = {}
                    order_db.save()
                    return render(request, 'orderplaced.html')     
        except:
            order_db.status = "Failed"
            request.session['cart'] = {}
            order_db.save()
            return render(request, 'orderfailed.html')
           