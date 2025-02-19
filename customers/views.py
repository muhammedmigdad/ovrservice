from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.db.models import Q, Sum
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
def index(request):
    store = Store.objects.all()
    reviews = Review.objects.all()
    storecategory = StoreCategory.objects.all()

    # Prepare the reviews with rating stars
    for review in reviews:
        review.star = int(review.rating)  # Adding star to each review
    
    context = {
        'store': store,
        'storecategory': storecategory,
        'reviews': reviews,
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
def products(request, id=None):
    storecategories = StoreCategory.objects.all()
    stores = Store.objects.all()
    products = Product.objects.all()  # Fetch all products by default

    # Store Filter Logic
    if id:  
        stores = stores.filter(id=id)
        products = products.filter(store_id=id)

    # Search Filter Logic
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)  # Search by name

    context = {
        'storecategories': storecategories,
        'stores': stores,
        'products': products,
        'search_query': search_query,  # Pass search query to template
    }
    
    return render(request, 'customer/products.html', context)



@login_required(login_url='/login/')
def profile(request):
    return render(request, 'customer/profile.html')

@login_required(login_url='/login/')
def product(request):
    return render(request, 'customer/product.html')






# def reviews_list(request):
#     reviews = Review.objects.all()  
#     return render(request, "customer/index.html", {"reviews": reviews})


# @login_required(login_url='/login/')
# def service(request):
#     services = Service.objects.all() 
#     # if not services.exists():
#     #     print("No services found!")  # Debugging
    
#     # cart_count = 0
#     # if request.user.is_authenticated:
#     #     customer = Customer.objects.filter(user=request.user).first()
#     #     if customer:
#     #         cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0

#     return render(request, 'customer/service.html', {"services": services})

@login_required(login_url='/login/')
def request_service(request):
    user = request.user
    services = Service.objects.all()

    # Search functionality
    query = request.GET.get('q')
    if query:
        services = services.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone')
        service_id = request.POST.get('service')
        details = request.POST.get('details')

        if not name or not phone or not service_id or not details:
            messages.error(request, "All fields are required")
            return redirect('customers:service')

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            messages.error(request, "Invalid service selected")
            return redirect('customers:service')

        ServiceRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service,
            details=details
        )

        messages.success(request, "Service request submitted successfully!")
        return redirect('customers:service')

    # Calculate cart count for authenticated users
    cart_count = 0
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            cart_count = CartItem.objects.filter(customer=customer).aggregate(total=Sum('quantity'))['total'] or 0

    context = {
        'cart_count': cart_count,
        'services': services,
        'query': query,  # Send query back to the template for input persistence
    }

    return render(request, 'customer/service.html', context)
@login_required(login_url='/login/')
def mechanic_service(request):
    """View for mechanics to manage service requests"""
    service_requests = ServiceRequest.objects.all().order_by('-created_datetime')

    context = {
        'service_requests': service_requests,
    }
    return render(request, 'customer/mechanic-service.html', context)

@login_required(login_url='/login/')
def mechanic_service_request(request, request_id):
    """Allow mechanics to update service request status"""
    user = request.user
    
    # Ensure only provider users can update requests
    if not ProviderUser.objects.filter(user=user).exists():
        messages.error(request, "Unauthorized access! You must be a provider to update service requests.")
        return redirect('customers:mechanic_service')

    # Fetch the service request
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        # Validate and update status
        if new_status in ['pending', 'in_progress', 'completed']:
            service_request.status = new_status
            service_request.save(update_fields=['status'])
            messages.success(request, "Service request status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('customers:mechanic-service')

@login_required(login_url='/login/')
def update_status(request, request_id):
    # Fetch the service request by ID
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    # Ensure the request method is POST
    if request.method == 'POST':
        new_status = request.POST.get('status')

        # Validate and update the status
        if new_status in ['pending', 'in_progress', 'completed']:
            service_request.status = new_status
            service_request.save(update_fields=['status'])
            messages.success(request, "Status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('customers:mechanic-service')  # Ensure this matches your URL name
