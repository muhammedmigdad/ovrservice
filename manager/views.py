from django.shortcuts import render, reverse, redirect, get_object_or_404
from providers.models import *
from spareparts.models import *
from django.http import HttpResponseRedirect, HttpResponse
from manager.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from common.functions import generate_form_errors
from common.decorators import allow_manager

@allow_manager
@login_required(login_url='/login/')
def index(request):
    
    return render(request,'manager/index.html')

def login(request):
    if request.method == "POST":
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_manager: 
                    auth_login  (request,user)
                    return redirect('manager:index') 
                else:
                    messages.error(request, "Unauthorized access.")
                    return HttpResponse("unauthorized", status=401)
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = ManagerLoginForm()

    return render(request, 'manager/login.html', {'form': form})

def logout(request):
    return redirect('manager:login')
        
    
@login_required(login_url='/login/')
def store(request):
    instances = Store.objects.all()
    context = {
        'instances': instances,
    }
    return render(request, 'manager/store.html', context=context)

@login_required(login_url='/login/')
def store_delete(request, id):
    instance = get_object_or_404(Store, id=id)
    instance.delete()
    messages.success(request, f"Store '{instance.name}' deleted successfully.")
    return HttpResponseRedirect(reverse('manager:store'))

@login_required(login_url='/login/')
def store_add(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Store added successfully.")
            return HttpResponseRedirect(reverse('manager:store'))
    else:
        form = StoreForm()
    
    context = {
        'form': form,
    }
    return render(request, 'manager/store_add.html', context=context)

@login_required(login_url='/login/')
def store_edit(request, id):
    instance = get_object_or_404(Store, id=id)

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Store '{instance.name}' updated successfully.")
            return HttpResponseRedirect(reverse('manager:store'))
    else:
        form = StoreForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'manager/store_add.html', context=context)
@allow_manager
@login_required(login_url='/login/')
def products(request):
    instances = Product.objects.all()
    context = {
        'instances': instances,
    }
    return render(request, 'manager/products.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def products_delete(request, id):
    instance = Product.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse('manager:products'))

@allow_manager
@login_required(login_url='/login/')
def products_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:products'))
        # No else needed—invalid form falls through to render
    else:
        form = ProductForm()

    context = {
        'form': form,
    }
    return render(request, 'manager/products_add.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def products_edit(request, id):
    instance = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:products'))
        # No else needed—invalid form falls through to render
    else:
        form = ProductForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'manager/products_add.html', context=context)
@allow_manager
@login_required(login_url='/login/')
def service_request(request):  # Pluralized for list view
    instances = ServiceRequest.objects.all()
    context = {
        'instances': instances,
    }
    return render(request, 'manager/service_request.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def service_request_delete(request, id):
    instance = ServiceRequest.objects.get(id=id)
    instance.delete()
    messages.success(request, f"Service request from '{instance.name}' deleted successfully.")
    return HttpResponseRedirect(reverse('manager:service_request'))

@allow_manager
@login_required(login_url='/login/')
def service_request_add(request):  # Removed unused 'id' parameter
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service request added successfully.")
            return HttpResponseRedirect(reverse('manager:service_request'))
        # Invalid form falls through to render
    else:
        form = ServiceRequestForm()

    context = {
        'form': form,
    }
    return render(request, 'manager/service_request_add.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def service_request_edit(request, id):
    instance = ServiceRequest.objects.get(id=id)
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Service request from '{instance.name}' updated successfully.")
            return HttpResponseRedirect(reverse('manager:service_request'))
        # Invalid form falls through to render
    else:
        form = ServiceRequestForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'manager/service_request_add.html', context=context)


@allow_manager
@login_required(login_url='/login/')
def service(request):  # Renamed to 'services' for consistency
    instances = Service.objects.all()
    context = {
        'instances': instances,
    }
    return render(request, 'manager/service.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def service_delete(request, id):
    instance = Service.objects.get(id=id)
    instance.delete()
    messages.success(request, f"Service '{instance.title}' deleted successfully.")
    return HttpResponseRedirect(reverse('manager:service'))

@allow_manager
@login_required(login_url='/login/')
def service_add(request):  # Removed unused 'id' parameter
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully.")
            return HttpResponseRedirect(reverse('manager:service'))
        # Invalid form falls through to render
    else:
        form = ServiceForm()

    context = {
        'form': form,
    }
    return render(request, 'manager/service_add.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def service_edit(request, id):
    instance = Service.objects.get(id=id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Service '{instance.title}' updated successfully.")
            return HttpResponseRedirect(reverse('manager:service'))
        # Invalid form falls through to render
    else:
        form = ServiceForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'manager/service_add.html', context=context)
@login_required(login_url='/login/')
def users(request):
    instances = User.objects.all()
    return render(request, 'manager/users.html', {'instances': instances})

@login_required(login_url='/login/')
def users_add(request):
    if request.method == 'POST':   
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manager:users')
    else:
        form = UserForm()
    
    return render(request, 'manager/users_add.html', {'form': form})

@login_required(login_url='/login/')
def users_edit(request, id):
    instance = get_object_or_404(User, id=id)
    if request.method == 'POST':   
        form = UserForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('manager:users')
    else:
        form = UserForm(instance=instance)
    
    return render(request, 'manager/users_add.html', {'form': form, 'instance': instance})

@login_required(login_url='/login/')
def users_delete(request, id):
    instance = get_object_or_404(User, id=id)
    instance.delete()
    return redirect('manager:users')

@allow_manager
@login_required(login_url='/login/')
def review(request):  # Pluralized for list view
    instances = Review.objects.all()
    context = {
        'instances': instances,
    }
    return render(request, 'manager/review.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def review_delete(request, id):
    instance = Review.objects.get(id=id)
    instance.delete()
    messages.success(request, f"Review from '{instance.name}' deleted successfully.")
    return HttpResponseRedirect(reverse('manager:review'))

@allow_manager
@login_required(login_url='/login/')
def review_add(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Review added successfully.")
            return HttpResponseRedirect(reverse('manager:review'))
        # Invalid form falls through to render
    else:
        form = ReviewForm()

    context = {
        'form': form,
    }
    return render(request, 'manager/review_add.html', context=context)

@allow_manager
@login_required(login_url='/login/')
def review_edit(request, id):
    instance = Review.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Review from '{instance.name}' updated successfully.")
            return HttpResponseRedirect(reverse('manager:review'))
        # Invalid form falls through to render
    else:
        form = ReviewForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'manager/review_add.html', context=context)
@allow_manager
@login_required(login_url='/login/')
def order(request):
    instances = Order.objects.all()
    return render(request, 'manager/order.html', {'instances': instances})

@allow_manager
@login_required(login_url='/login/')
def order_delete(request, id):
    instance = get_object_or_404(Order, id=id)
    instance.delete()
    return redirect('manager:order')

@allow_manager
@login_required(login_url='/login/')
def order_add(request):
    if request.method == 'POST':   
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manager:order')
        else:
            message = generate_form_errors(form)  # ✅ Keep form data
    else:
        form = OrderForm()

    return render(request, 'manager/order_add.html', {'form': form})



    




    
