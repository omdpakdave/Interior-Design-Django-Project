from django.contrib import admin
from .models import *
from .models import Order 

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)

# Register your models here.
