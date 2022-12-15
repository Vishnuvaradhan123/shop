from django.contrib import admin
from django.urls import path
from .views import Index , store
from .views import Signup
from .views  import Login,logout
from .views import Cart
from .views  import CheckOut
from .views  import OrderView
from .middlewares.auth import  auth_middleware
from . import views

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store',store, name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    # path('login',views.login,name="login"),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('<int:id>/detail/',views.detail_page,name='detail'),
    path('search',views.search,name="search"),

    path('forgot_password', views.forgot_password ,name='forgot_password'),
    path('reset_password', views.reset_password ,name='reset_password'),
    path('send_otp',views.send_otp,name='send_otp'),
    path('paytm', views.paytm , name="paytm"),
    path('paymentstatus',views.paymentstatus,name='paymentstatus'),
   
    path('profile/<str:customer>', views.view_profile, name='profile'),
    path('profile/<str:customer>/settings', views.settingss, name='settings'),
    path('update_profile/<current_customer>', views.update_profile, name='update_profile'),
    path('address/<current_customer>',views.address,name='address'),
    # path('checkout/',views.checkout,name="checkout"),
    path('paymenthandler/',views.paymenthandler,name="paymenthandler"),
    path('new/',views.checkout,name="checkout"),
    path('fail/',views.paymentfail,name="paymentfail"),
]
