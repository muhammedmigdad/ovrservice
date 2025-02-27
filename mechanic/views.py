from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from common.decorators import allow_manager
from common.functions import generate_form_errors
from django.core.validators import EmailValidator, ValidationError
from users.models import User
from providers.models import *
from datetime import datetime
from customers.models import *
from spareparts.models import *
import uuid
User = get_user_model()  # Ensure using custom user model



# ✅ Signup View


@login_required(login_url="/app/login")
def index(request):    

    return render(request, "mechanic/index.html")





def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("managers:login"))


def mechanic_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect("providers:mechanic-login")

        user = authenticate(request, email=email, password=password)  # Authenticate using email

        if user is not None:
            if hasattr(user, "is_provider") and user.is_provider:  # Ensure user has `is_provider`
                login(request, user)
                messages.success(request, "Mechanic login successful!")
                return redirect("providers:dashboard")  # Redirect to mechanic dashboard
            else:
                messages.error(request, "You are not authorized as a mechanic.")
        else:
            messages.error(request, "Invalid email or password.")

        return redirect("providers:mechanic-login")

    return render(request, "provider/mechanic-login.html")


@login_required(login_url='/login/')
def user_logout(request):
    auth_logout(request)
    return redirect('customers:index') 


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
