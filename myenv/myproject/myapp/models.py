from django.db import models
from django.utils import timezone


class User(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    mobile=models.IntegerField(unique=True)
    password=models.CharField(max_length=10)
    profile = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True
    )
    usertype = models.CharField(max_length=20,default="customer")

    def  __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    dname=models.CharField(max_length=40)
    dprice=models.IntegerField()
    desc=models.TextField()
    dprofile = models.ImageField(
        upload_to='dprofile/',
        blank=True,
        null=True
    )
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
 


    def  __str__(self):
        return f"{self.dname}"


class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.dname}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.product.dname

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    total = models.IntegerField()
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="Paid")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name