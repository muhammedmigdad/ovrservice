from django.urls import path
from providers import views

app_name = "providers"

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("bill/", views.bill_view, name="bill"),
    path("traking/", views.traking_view, name="traking"),
    path("mechanic-login/", views.mechanic_login, name="mechanic-login"),
    path("service_request_delete/<int:id>/", views.service_request_delete, name="service_request_delete"),
]
