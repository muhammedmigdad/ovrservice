from django.urls import path
from mechanic import views

app_name = 'mechanics'

urlpatterns = [

    path("", views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    
    
    
    path('mechanic-service/', views.mechanic_service, name='mechanic-service'),
    path('mechanic-service-requst/<int:request_id>/', views.mechanic_service_request, name='mechanic-service-requst'),
    path('update_status/<int:request_id>/', views.update_status, name='update_status'),
    
]