from django.urls import path
from providers import views

app_name = "providers"

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("mechanic-login/", views.mechanic_login, name="mechanic-login"),
    path("mechanic-service/", views.mechanic_service, name="mechanic-service"),
    path("mechanic-service-request/<int:request_id>/", views.mechanic_service_request, name="mechanic-service-request"),
]
