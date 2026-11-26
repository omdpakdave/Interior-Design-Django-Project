from http import client
from django.shortcuts import render, redirect
from .models import *
import random
from django.conf import settings
from django.core.mail import send_mail
from .models import Product,Wishlist
import razorpay
from django.conf import settings
from django.shortcuts import render

client = razorpay.Client(auth=(
    settings.RAZORPAY_KEY_ID,
    settings.RAZORPAY_KEY_SECRET
))

def index(request):
    return render(request,'index.html')


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def blog_html(request):
    return render(request, 'bloghome.html')


def blog_single(request):
    return render(request, 'blogsingle.html')


def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            msg = "Email already exists"
            return render(request, 'signup.html', {'msg': msg})

        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    password=request.POST['password'],
                    profile=request.FILES['profile'],
                    usertype=request.POST['usertype']
                )

                msg = "Sign up successfully"
                return render(request, 'signup.html', {'msg': msg})

            else:
                msg = "Password and confirm password does not match"
                return render(request, 'signup.html', {'msg': msg})

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])

            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['profile'] = user.profile.url
                if user.usertype=="customer":
                    return redirect('index')
                else:
                    return redirect('aindex')


            else:
                msg = "Password does not match"
                return render(request, 'login.html', {'msg': msg})

        except User.DoesNotExist:
            msg = "Email does not exist"
            return render(request, 'login.html', {'msg': msg})

    return render(request, 'login.html')


def logout(request):
        del request.session['email']   
        del request.session['profile']   

        return redirect('index')




def fpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])

            # Generate OTP
            otp = random.randint(1001, 9999)

            # Email Details
            subject = "OTP for Forgot Password"

            message = f"""
Dear {user.name},

We received a request to reset the password for your account.

To proceed with resetting your password, please use the One-Time Password (OTP) below:

OTP: {otp}

This OTP is valid for 10 minutes.

For security reasons, please do not share this OTP with anyone.

Thank you,

DJANGO PROJECT
"""

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(
                subject,
                message,
                email_from,
                recipient_list,
                fail_silently=False
            )

            request.session['email'] = user.email
            request.session['otp'] = otp

            return render(request, 'otp.html')

        except User.DoesNotExist:
            msg = "Email does not exist"
            return render(request, 'fpass.html', {'msg': msg})

    return render(request, 'fpass.html')

def otp(request):
    if request.method=="POST":
        try:
            otp=int(request.session['otp'])
            uotp=int(request.POST['uotp'])

            if otp==uotp:
                del request.session['otp']
                return redirect('newpass')
            else:
                msg="Invalid OTP"
                return render(request,'otp.html',{'msg':msg})
        except Exception as e:
            print("OTP Error:", e)
            msg = "Something went wrong. Please try again."
            return render(request, 'otp.html', {'msg': msg})
    else:
        return render(request,'otp.html')
    
def newpass(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.session['email'])
            if request.POST['password']==request.POST['cnpassword']:
                user.password = request.POST['password']
                user.save()
                del request.session['email']
                return redirect('login')
            else:
                msg = "Password and confirm password does not match"
                return render (request,'newpass.html',{'msg':msg})
        except Exception as e:
            print("newpass Error:", e)
            msg = "Session expired or an error occurred. Please try again."
            return render(request, 'newpass.html', {'msg': msg})
    else:
        return render (request,'newpass.html')

        
def cpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.session['email'])

            if user.password==request.POST['opassword']:
                if request.POST['npassword']==request.POST['cnpassword']:
                    user.password = request.POST['npassword']
                    user.save()
                    return redirect('login')
                else:
                    msg = "New password & confirm new password does not match!!"    
                    return render(request,'cpass.html',{'msg':msg})
            else:
                msg = "Old password does not match!!"
                return render(request,'cpass.html',{'msg':msg})
            
        except Exception as e:
            print("********************",e)
            return redirect('index')

    else:
        
        return render(request,'cpass.html')
    



def uprofile(request):
    user = User.objects.get(email=request.session['email'])

    if request.method == "POST":
        user.name = request.POST.get('name')
        user.mobile = request.POST.get('mobile')

        if 'profile' in request.FILES:
            user.profile = request.FILES['profile']

        user.save()

        # Update session after saving
        if user.profile:
            request.session['profile'] = user.profile.url

        return redirect('index')

    return render(request, 'uprofile.html', {'user': user})

def aindex(request):
        return render(request,'aindex.html')


def add(request):
        if request.method=="POST":
            try:
                user = User.objects.get(email=request.session['email'])
                Product.objects.create(
                    dname=request.POST['dname'],
                    dprice=request.POST['dprice'], 
                    desc=request.POST['desc'],
                    dprofile=request.FILES.get('dprofile'),
                    is_active=True,
                    user=user
                )
                
                msg="Product added successfully"
                return render(request, 'add.html', {'msg': msg})
            except Exception as e:
                print("add Error:", e)
                msg = "Failed to add product. Please check your session or input."
                return render(request, 'add.html', {'msg': msg})
        else:
            return render(request,'add.html')


def view(request):
    user=User.objects.get(email=request.session['email'])
    product = Product.objects.filter(user=user)
    return render(request,'view.html',{'product':product})

def delete(request,pk):
     user=User.objects.get(email=request.session['email'])
     product = Product.objects.get(pk=pk)
     product.delete()
     return redirect('aindex')

def update(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == "POST":
        product.dname = request.POST['dname']
        product.desc = request.POST['desc']

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('view')

    return render(request, 'update.html', {'product': product})

def cview(request):
    product = Product.objects.all()
    return render(request,'cview.html',{'product':product})

def addwish(request, pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)

    Wishlist.objects.get_or_create(
        user=user,
        product=product
    )

    return redirect('wishlist')

def wishlist(request):
     user = User.objects.get(email=request.session['email'])
     wishlist = Wishlist.objects.filter(user=user)
     request.session['wishlist'] = len(wishlist)
     return render(request,'wishlist.html',{'wishlist':wishlist})

def dwish(request,pk):
     user = User.objects.get(email=request.session['email'])
     product = Product.objects.get(pk=pk)
     w = Wishlist.objects.get(user=user,product=product)
     w.delete()
     return redirect('wishlist')

def addcart(request, pk):

    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)

    cart, created = Cart.objects.get_or_create(
        user=user,
        product=product
    )

    if not created:
        cart.qty += 1
        cart.save()

    request.session['cart'] = Cart.objects.filter(user=user).count()


    return redirect('cart')

def cart(request):

    user = User.objects.get(email=request.session['email'])

    cart = Cart.objects.filter(user=user)

    request.session['cart'] = cart.count()


    total = 0

    for i in cart:
        total += i.product.dprice * i.qty

    return render(request,'cart.html',{
        'cart':cart,
        'total':total
    })


def deletecart(request, pk):

    user = User.objects.get(email=request.session['email'])

    Cart.objects.filter(pk=pk).delete()

    request.session['cart'] = Cart.objects.filter(user=user).count()

    return redirect('cart')

def increase(request, pk):

    cart = Cart.objects.get(pk=pk)

    cart.qty += 1

    cart.save()

    return redirect('cart')

def decrease(request, pk):

    cart = Cart.objects.get(pk=pk)

    if cart.qty > 1:
        cart.qty -= 1
        cart.save()

    return redirect('cart')

def myorder(request):
    user = User.objects.get(email=request.session['email'])

    orders = Order.objects.filter(user=user).order_by('-id')

    return render(request, 'myorder.html', {
        'orders': orders
    }) 

def payment(request):

    amount = 50000

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "payment": payment,
        "amount": amount,
        "key": settings.RAZORPAY_KEY_ID,
    }

    return render(request, "payment.html", context)


def payment_success(request):
    if request.method == "POST":

        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")

        user = User.objects.get(email=request.session['email'])

        cart = Cart.objects.filter(user=user)

        for i in cart:
            Order.objects.create(
                user=user,
                product=i.product,
                qty=i.qty,
                total=i.product.dprice * i.qty,
                payment_id=payment_id,
                order_id=order_id,
                status="Paid"
            )

        cart.delete()
        request.session['cart'] = 0

        return redirect('myorder')

    return redirect('cart')