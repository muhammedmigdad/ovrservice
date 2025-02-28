from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from providers.models import ProviderServiceRequest

User = get_user_model()  # ✅ Ensure using the custom user model


@login_required(login_url="/app/mechanic-login/")
def index(request):
    """Mechanic dashboard"""
    return render(request, "mechanic/index.html")  # ✅ Ensure this template exists


def mechanic_login(request):
    """Handles mechanic login."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect(reverse("providers:mechanic-login"))

        user = authenticate(request, email=email, password=password)

        if user is not None and getattr(user, "is_provider", False):
            auth_login(request, user)
            messages.success(request, "Mechanic login successful!")
            return redirect(reverse("providers:index"))
        else:
            messages.error(request, "Invalid email or not authorized as a mechanic.")

    return render(request, "mechanic/mechanic-login.html")  # ✅ Ensure this template exists


def logout_view(request):
    """Logs out the mechanic and redirects to login page."""
    auth_logout(request)
    return redirect(reverse("mechanic:mechanic-login"))


@login_required(login_url="/app/mechanic-login/")
def mechanic_service(request):
    """View for mechanics to manage service requests"""
    service_requests = ProviderServiceRequest.objects.all().order_by("-created_datetime")
    return render(request, "mechanic/mechanic-service.html", {"service_requests": service_requests})


@login_required(login_url="/app/mechanic-login/")
def mechanic_service_request(request, request_id):
    """Allow mechanics to update service request status"""
    service_request = get_object_or_404(ProviderServiceRequest, id=request_id)

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in ["pending", "in_progress", "completed"]:
            service_request.status = new_status
            service_request.save(update_fields=["status"])
            messages.success(request, "Service request status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect("providers:mechanic-service")
