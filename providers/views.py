from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from providers.models import *
from django.http import HttpResponseRedirect, HttpResponse
from spareparts.models import *
from .forms import *  # ✅ Import the correct form
from common.functions import generate_form_errors
from common.decorators import allow_provider


User = get_user_model()  # ✅ Ensure using the custom user model


def mechanic_login(request):
    if request.method == "POST":
        form = MechanicLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            print(f"Form Data: Email={email}, Password={password}")
            print(f"Authenticated User: {user}")
            if user is not None:
                print(f"User is_provider: {getattr(user, 'is_provider', False)}")

                if getattr(user, "is_provider", False):
                    auth_login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect("providers:index")
                else:
                    messages.error(request, "Unauthorized access.")
                    return redirect("providers:mechanic-login")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Form is invalid.")
    else:
        form = MechanicLoginForm()

    return render(request, "mechanic/mechanic-login.html", {"form": form})

def logout_view(request):
    return redirect('providers:mechanic-login')


allow_provider
@login_required(login_url="/app/mechanic-login/")
def index(request):
    instances = ServiceRequest.objects.all()  # Fixed model reference
    context = {
        'instances': instances,  # Use 'instances' in the template
    }
    """Mechanic dashboard"""
    return render(request, "mechanic/index.html", context=context)  # ✅ Ensure this template exists


allow_provider
@login_required(login_url='/login/')
def service_request_delete(request, id):
    instance = get_object_or_404(ServiceRequest, id=id)  # Fixed model reference
    instance.delete()
    messages.success(request, f"Service request from '{instance.name}' deleted successfully.")
    return redirect('mechanic:index')  # Ensure 'mechanic:index' is a valid URL


def bill_view(request):
    
    return render(request, "mechanic/bill.html") 


def traking_view(request):
    
    return render(request, "mechanic/traking.html") 

