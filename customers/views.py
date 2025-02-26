from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
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
            return redirect("providers:mechanic-login")  # Redirect providers to login

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
            return redirect("providers:mechanic-login")

        user = authenticate(request, email=email, password=password)  # Authenticate using email

        if user is not None and user.is_provider:  # Ensure only providers can log in
            login(request, user)
            messages.success(request, "Mechanic login successful!")
            return redirect("providers:dashboard")  # Ensure correct redirection
        else:
            messages.error(request, "Invalid credentials or not authorized as a mechanic.")
            return redirect("providers:mechanic-login")

    return render(request, "provider/mechanic-login.html")

@login_required(login_url='/login/')
def user_logout(request):
    auth_logout(request)
    return redirect('customers:index') 

def otp(request):
    return render(request, 'customer/otp.html')


@login_required(login_url='/login/')
def mechanic_dashboard(request):
    
    return render(request, 'mechanic/dashbord.html')

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
def client_account(request):
    return render(request, 'customer/client-account.html')


@login_required(login_url='/login/')
def contact(request):
    return render(request, 'customer/contact.html')

def notification(request):
    return render(request, 'customer/notification.html')

def products(request, id=None):
    storecategories = StoreCategory.objects.select_related('store').all()  # Ensures store details are fetched
    stores = Store.objects.all()
    products = Product.objects.all()  

    if id:  
        stores = stores.filter(id=id)
        products = products.filter(store_id=id)

    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {
        'storecategories': storecategories,
        'stores': stores,
        'products': products,
        'search_query': search_query,
    }
    
    return render(request, 'customer/products.html', context)



@login_required(login_url='/login/')
def store(request, category_id=None):
    storecategories = StoreCategory.objects.all()
    products = Product.objects.all()  # Fetch all products by default

    # Filter products by store category if a category_id is provided
    if category_id:
        products = products.filter(store__storecategory__id=category_id)

    # Search Filter Logic
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)  # Search by product name

    context = {
        'storecategories': storecategories,
        'products': products,
        'search_query': search_query,  # Pass search query to template
    }
    
    return render(request, 'customer/products.html', context=context)


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'customer/profile.html')

@login_required(login_url='/login/')
def product_detail(request, product_id):
    """
    Displays product details and cart totals.
    """
    user = request.user
    customer, _ = Customer.objects.get_or_create(user=user)
    product = get_object_or_404(Product, id=product_id)

    # Fetch cart items for the customer
    cart_items = CartItem.objects.filter(customer=customer)

    # Update cart totals
    update_cart_total(customer)

    # Fetch the updated cart total
    cart_total = CartTotal.objects.get(customer=customer)

    # Prepare context for the template
    context = {
        'cart_total': cart_total,
        'cart_items': cart_items,
        'product': product,
    }
    return render(request, 'customer/product.html', context)
def update_cart_total(customer):
    cart_items = CartItem.objects.filter(customer=customer)

    # Calculate item total based on cart items
    item_total = sum(
        (item.product.sale_price if item.product.sale_price else item.product.regular_price) * item.quantity
        for item in cart_items
    )
    
    tax_charge = item_total * 0.10  # 10% tax
    total = item_total + tax_charge

    # ✅ Ensure cart_total updates correctly
    cart_total, created = CartTotal.objects.get_or_create(customer=customer)

    cart_total.item_total = item_total  # ✅ Update item_total
    cart_total.tax_charge = tax_charge  # ✅ Update tax_charge
    cart_total.total = total  # ✅ Update total
    cart_total.save()  # ✅ Save the updated values





@login_required(login_url='/login/')
def add_cart(request, id):
    """
    Adds a product to the cart.
    """
    customer = Customer.objects.get(user=request.user)
    product = Product.objects.get(id=id)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': 1, 'price': product.price}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.price = cart_item.quantity * product.price
        cart_item.save()

    # Update cart totals
    update_cart_total(customer)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def cart_plus(request, id):
    """
    Increases the quantity of a product in the cart.
    """
    customer = Customer.objects.get(user=request.user)
    product = get_object_or_404(Product, id=id)

    # Use sale_price if available, otherwise use regular_price
    product_price = product.sale_price if product.sale_price else product.regular_price

    cart_item, created = CartItem.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': 1, 'price': product_price}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.price = cart_item.quantity * product_price
        cart_item.save()

    update_cart_total(customer)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def cart_minus(request, id):
    """
    Decreases the quantity of a product in the cart.
    Removes the product if the quantity reaches zero.
    """
    customer = Customer.objects.get(user=request.user)
    product = get_object_or_404(Product, id=id)
    cart_item = get_object_or_404(CartItem, customer=customer, product=product)

    product_price = product.sale_price if product.sale_price else product.regular_price

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.price = cart_item.quantity * product_price
        cart_item.save()
    else:
        cart_item.delete()

    update_cart_total(customer)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  


@login_required(login_url='/login/')
def checkout(request):
    """
    Handles the checkout process for the customer.
    """
    customer = Customer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    cart_total = CartTotal.objects.filter(customer=customer).first()

    # Check if the cart is empty
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('customers:cart_view')

    if request.method == 'POST':
        # Extract form data
        payment_method = request.POST.get('payment')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        # Validate required fields
        required_fields = [first_name, last_name, email, phone_number]
        if not all(required_fields):
            messages.error(request, "Please fill in all required fields.")
            return redirect('customers:checkout')

        # Validate payment method
        valid_payment_methods = ['credit_card', 'net_banking', 'cod']
        if payment_method not in valid_payment_methods:
            messages.error(request, "Please select a valid payment method.")
            return redirect('customers:checkout')

        # Ensure cart total exists
        if not cart_total:
            messages.error(request, "Error processing your order. Please try again.")
            return redirect('customers:cart_view')

        # Create the order
        try:
            order = Order.objects.create(
                customer=customer,
                order_id=str(uuid.uuid4().hex[:10]),  # ✅ Generate unique order ID
                total=cart_total.total,
                payment_method=payment_method,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                city=city,
                state=state,
                pincode=pincode
            )

            # Move cart items to OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    customer=customer,
                    product=item.product,
                    quantity=item.quantity,
                    amount=item.product.sale_price if item.product.sale_price else item.product.regular_price
                )
                item.delete()  # ✅ Remove cart item after order placement

            # Clear cart total after order is placed
            cart_total.delete()  # ✅ Remove cart total after order placement

            messages.success(request, "Order placed successfully!")
            print("Redirecting to order_success...")  # ✅ Debugging print
            return redirect('customers:order_success')  # ✅ Make sure this URL exists

        except Exception as e:
            messages.error(request, f"An error occurred while processing your order: {str(e)}")
            return redirect('customers:checkout')

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, 'customer/checkout.html', context=context)

@login_required(login_url='/login/')
def order_success(request):
    return render(request, 'customer/ordersucces.html')


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
    return render(request, 'mechanic/mechanic-service.html', context)

@login_required(login_url='/login/')
def mechanic_service_request(request, request_id):
    """Allow mechanics to update service request status"""
    user = request.user
    
    # Ensure only provider users can update requests
    if not ProviderUser.objects.filter(user=user).exists():
        messages.error(request, "Unauthorized access! You must be a provider to update service requests.")
        return redirect('mechanics:mechanic_service')

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

    return redirect('mechanics:mechanic-service')

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

    return redirect('mechanics:mechanic-service')  # Ensure this matches your URL name
