from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,logout
from django.contrib.auth.models import User as U,auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import math, random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.urls import reverse_lazy, reverse
from django.shortcuts import render , redirect ,HttpResponseRedirect,HttpResponse
from .models import Products,Order,Customer,Category
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import  make_password
import json
from django.views import  View
import math,random
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
import razorpay

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# def address(request):
#     add = Customer.objects.filter(email=request.user)

#     return render(request,'address.html',{'add':add})

def forgot_password(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST['email']
        # print(email)
        
        if Customer.objects.filter(email=email).exists():

                email= request.POST.get('email')
                request.session.get('email')
                return redirect('forgot_password')
        else:
            messages.info(request,"email is already exists")
            return redirect('change_password')
    return render(request,'forgot_password.html')

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     print(OTP)
     return OTP

def send_otp(request):
   
     email=request.POST.get("email")
     request.session['email']=email
     print(email)   
     o=generateOTP()
     htmlgen = '<p>Your OTP is <strong>o</strong></p>'
     send_mail(
      subject="Reset Forget password", 
      message= f'OTP request {o}',
      from_email=settings.EMAIL_HOST_USER,
      recipient_list=[email],
      )
     return HttpResponse(o)

     
def reset_password(request):
    if request.method=='POST':
        nw=request.POST.get('nw')
        print(nw)
        cw= request.POST.get('cw')
        print(cw)
        email = request.session.get("email")
        print("--------------------------",email)
        try: 
            print('#######')
            u=Customer.objects.get(email=email)
            u.password=cw
            u.save()
            print(u)
            print("password changed")
            return redirect('login')
        except ObjectDoesNotExist:
            return HttpResponse("changing password is not working")
    else:
        return render(request,'reset_password.html')



def search(request):
        query = request.GET.get('query')
        search_category_products = Products.objects.filter(category__name__icontains=query)
        search_id = Products.objects.filter(id__icontains=query)
        search_name = Products.objects.filter(name__icontains=query)
        search_result = search_id.union(search_name,search_category_products)

        param = {'search_result': search_result, 'search_term':query}
        return render(request, 'search.html', param)

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products} )
    
    
def detail_page(request,id):
    products = Products.objects.filter(id=id)
    context={'products':products}
    return render(request,'detail.html',context)

def reviews(request,slug):
    if request.method == "POST" and request.User.is_authenticated:
        products = get_object_or_404(Products,slug=slug)
        stars = request.POST.get('stars',4)
        content = request.POST.get('content','')
        print(stars,content)
        review = ProductReview.objects.create(products=products,User=request.User,stars=stars, content=content)
        print(review)
        review.save()
    return redirect("details",id=id)

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        return redirect('checkout')
class Index(View):
    
    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')

    def get(self , request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def store(request):
    cart = request.session.get('cart')
   
    if not cart:
        request.session['cart'] = {}
    products = None
    
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories
    
    return render(request, 'index.html', data)


def logout(request):
    request.session.clear()
    return redirect('login')
class OrderView(View):
    

    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})

def paytm(request):
    return render(request,'paytm.html')
def paymentstatus(request):
    return render(request,'paymentstatus.html')

# def profile(request):
#     if request.method == 'POST':
#         customer = Customer.objects.all()

#         fname = request.POST.get('fname')
#         lname = request.POST.get('lname')
        
#         phone = request.POST.get('phone')


#         customer = Customer(first_name = fname,
#         last_name = lname,
       
#         phone = phone)
#         customer.save()
#     return render(request,"profile.html")
def address(request,current_customer):
    if request.method == 'POST':
        name = Customer.objects.all()
        locality = Customer.objects.all()
        street = Customer.objects.all()
        city = Customer.objects.all()
        state = Customer.objects.all()
        zip = Customer.objects.all()


        customer = Customer(name=name,
        locality=locality,
        street=street,
        state=state,
        city=city,
        zip=zip)


        customer.save()
            
    return render(request,"address.html")
    
class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None
        
        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer (customer)

        if not error_message:
            print (first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            customer.register ()
            return redirect ('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')            
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                
                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'login.html', {'error': error_message})
def view_profile(request, customer):
    try:
        customer_obj = Customer.objects.get(id=customer)
    except ObjectDoesNotExist:
        return HttpResponse('User does not exists.')

    
    param = { 'customer_data': customer_obj}
    try:
        return render(request, 'profile.html', param)
    except:
        messages.warning(request, f"You have to login before access {customer}'s profile.")
        return redirect('home')


def update_profile(request, current_customer):
    if request.method == 'POST':
        get_customer = Customer.objects.get(id=current_customer)

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mail = request.POST.get('mail')
       


        get_customer.first_name = fname
        get_customer.last_name = lname
        get_customer.email = mail
      
        get_customer.save()
        return redirect('homepage')
    else:
        return redirect('profile')





def settingss(request, customer):
    get_customer = Customer.objects.get(id=customer)


    if request.method == 'POST':
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        


        if (pwd1 and pwd2) :
            if pwd1==pwd2:
                get_customer.password = pwd1
                get_customer.save()
                messages.success(request, 'Password saved succesfully.')
            else:
                messages.warning(request, 'Password are not same.')
       

    param = {'user_data': get_customer}
    return render(request, 'profile_settings.html', param)



def delete_user(request, user):
    if request.method == 'POST':
        get_customer = User.objects.get(first_name=user)

        firstName = request.POST.get('first_name')
        if firstName == get_customer.first_name:
            get_customer.delete()
            del request.session['user']
            return redirect('home')

    return HttpResponseRedirect(reverse('settings', args=[str(user)]))
# def login(request):
#     if request.method == "POST":
       
#         password = request.POST['password']
#         email= request.POST.get('email')
#         request.session['email']=email
#         print(request.session.get('email'))
#         print(password)
#         # Customer = authenticate(email=email, password=password)
#         if Customer is not None:
            
#             auth.login(request, Customer)
#             return redirect("home")
#         else:
#             messages.info(request,"Invalid username")
#             return redirect("login")
#     return render(request,'login.html')

def checkout(request):
    # user = request.user
    # first_name = request.user
    # email = Customer.objects.filter(first_name=first_name)
    # cart_items  = Cart.objects.filter(user=user)
    # amount = 0
    # shipping_amount = 70
    # cart_product = [p for p in Cart.objects.all() if p.user == user]

    # if cart_product:
    #     for p in  cart_product:
    #         temp_amount = (p.quantity * p.product.discounted_price)
    #         amount += int(temp_amount)
    #         total_amount = amount + shipping_amount 
    
    currency = "INR"
    amount = 20000

    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture="0"))

    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    context={}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    # context['email'] = email
    # context['cart_items'] = cart_items
    # context['total_amount'] = total_amount
    return render(request,'test.html', context=context)

     

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id','')
            razorpay_order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature')
            params_dict={
                'razorpay_order_id':razorpay_order_id,
                'razorpay_payment_id':payment_id,
                'razorpay_signature':signature
            }

            result = razorpay_client.utility.verify_payment_signature(
                params_dict
            )
            if result is not None:
                amount = 20000
                try:
                    razorpay_client.payment.capture(payment_id,amount)
                    return render(request,'paymentsuccess.html')
                except:
                    return render(request,'paymentfail.html')
            else:
                return render(request,"paymentfail.html")
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

def paymentfail(request):
    return render(request,'paymentfail.html')
