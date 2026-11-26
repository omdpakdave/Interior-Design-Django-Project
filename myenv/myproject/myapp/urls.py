"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('bloghtml/',views.blog_html,name='bloghtml'),
    path('fpass/',views.fpass,name='fpass'),
    path('otp/',views.otp,name='otp'),
    path('newpass/',views.newpass,name='newpass'),
    path('cpass/',views.cpass,name='cpass'),
    path('uprofile/',views.uprofile,name='uprofile'),
    path('aindex/', views.aindex, name='aindex'),
    path('add/', views.add, name='add'),
    path('view/', views.view, name='view'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('cview/', views.cview, name='cview'),
    path('addwish/<int:pk>/', views.addwish, name='addwish'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('dwish/<int:pk>/', views.dwish, name='dwish'),
    path('addcart/<int:pk>/', views.addcart, name='addcart'),
    path('cart/', views.cart, name='cart'),
    path('deletecart/<int:pk>/', views.deletecart, name='deletecart'),
    path('increase/<int:pk>/', views.increase, name='increase'),
    path('decrease/<int:pk>/', views.decrease, name='decrease'),
    path('payment/', views.payment, name='payment'),
    path('myorder/', views.myorder, name='myorder'),
    path('payment-success/', views.payment_success, name='payment_success')

    
    

          
]
