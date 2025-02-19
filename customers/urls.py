from django.urls import path
from customers import views

app_name = 'customers'

urlpatterns = [
    path("", views.index, name="index"),

    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("mechanic-login/", views.mechanic_login, name="mechanic-login"),
    path('logout/', views.user_logout, name='logout'),

    
    path("otp/", views.otp, name="otp"),
    
    path("profile/", views.profile, name="profile"),
    path("checkout/", views.checkout, name="checkout"),
    path("client-bill/", views.client_bill, name="client-bill"),
    
    path("contact/", views.contact, name="contact"),
    path("notification/", views.notification, name="notification"),
    path('products/<int:id>/', views.products, name='products'),
    path("product/", views.product, name="product"),
    
    path('service/', views.request_service, name='service'),
    # path('reviews/', views.reviews_list, name='reviews_list'),
    path('mechanic-service/', views.mechanic_service, name='mechanic-service'),
    path('mechanic-service-requst/<int:request_id>/', views.mechanic_service_request, name='mechanic-service-requst'),
    path('update_status/<int:request_id>/', views.update_status, name='update_status'),
    
]