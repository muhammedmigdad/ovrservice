from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from common.decorators import allow_manager
from common.functions import generate_form_errors
from users.models import User
from providers.models import *
from customers.models import *
from spareparts.models import *

User = get_user_model()  # Ensure using custom user model



# ✅ Signup View
def signup(request):    
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        user_type = request.POST.get("userType", "client")  # Default to client

        if not name or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("customers:signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("customers:signup")

        # ✅ Create the user
        user = User(email=email)
        user.set_password(password)  # Hash password
        user.first_name = name

        # ✅ Assign user type
        if user_type == "client":
            user.is_customer = True
        elif user_type == "mechanic":
            user.is_provider = True  # Assuming "provider" is a mechanic

        user.save()

        messages.success(request, "Account created successfully. Please log in.")

        if user_type == "client":
            return redirect("customers:login")
        else:
            return redirect("customers:mechanic-login")  # Redirect mechanics to login

    return render(request, "customer/signup.html")

# ✅ Login View (Client & Mechanic)
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect("customers:login")

        try:
            user = User.objects.get(email=email)  # Get user by email
            user = authenticate(request, username=user.email, password=password)  # Use email as username
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("customers:index")  # Redirect after login
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("customers:login")

    return render(request, "customer/login.html")

# ✅ Mechanic Login View
def mechanic_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect("customers:mechanic-login")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.email, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_provider:  # Ensure only mechanics can login here
            login(request, user)
            messages.success(request, "Mechanic login successful!")
            return redirect("customers:index")  # Redirect to mechanic dashboard
        else:
            messages.error(request, "Invalid credentials or not authorized as a mechanic.")
            return redirect("customers:mechanic-login")

    return render(request, "customer/mechanic-login.html")

@login_required(login_url='/login/')
def user_logout(request):
    auth_logout(request)
    return redirect('customers:index') 

def otp(request):
    return render(request, 'customer/otp.html')



@login_required(login_url='/login/')
def index(request, id):
    store = Store.objects.all()
    
    storecategory = StoreCategory.objects.all()
    
    
    context = {
        'store': store,
       'storecategory': storecategory
    }
    
    return render(request, 'customer/index.html', context=context)



@login_required(login_url='/login/')
def checkout(request):
    return render(request, 'customer/checkout.html')


@login_required(login_url='/login/')
def client_bill(request):
    return render(request, 'customer/client-bill.html')


@login_required(login_url='/login/')
def contact(request):
    return render(request, 'customer/contact.html')

def notification(request):
    return render(request, 'customer/notification.html')

@login_required(login_url='/login/')
def products(request):
    return render(request, 'customer/products.html')

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'customer/profile.html')

@login_required(login_url='/login/')
def product(request):
    return render(request, 'customer/product.html')



@login_required(login_url='/login/')
def service(request):
    return render(request, 'customer/service.html')


@login_required(login_url='/login/')
def store(request):
    return render(request, 'customer/store.html')