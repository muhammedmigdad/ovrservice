from django.urls import path
from customers import views

app_name = 'providers'

urlpatterns = [

    path("mechanic-login/", views.mechanic_login, name="mechanic-login"),
    path("dashboard/", views.mechanic_dashboard, name="dashboard"),  # Ensure this view exists
    
    
]