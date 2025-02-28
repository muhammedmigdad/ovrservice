from django.urls import path
from customers import views

app_name = 'customers'

urlpatterns = [
    path("", views.index, name="index"),

    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path('logout/', views.user_logout, name='logout'),

    
    path("otp/", views.otp, name="otp"),
    
    path('orders/<int:id>/', views.orders, name='orders'),
    path("order-item/", views.order_item, name="order-item"),
    
    path("client-account/", views.client_account, name="client-account"),
    path('account/edit/', views.edit_profile, name='edit_profile'),
    
    
    path("checkout/", views.checkout, name="checkout"),
    path('payment/', views.payment, name='payment'),
    path('order-success/', views.order_success, name='order_success'),
    
    path("contact/", views.contact, name="contact"),
    path("notification/", views.notification, name="notification"),
    path("tracking/", views.tracking, name="tracking"),
    
    
    path('products/<int:id>/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    
    path("cart/add/", views.add_cart, name="add_cart"),
    path("cart/plus/<int:id>/", views.cart_plus, name="cart_plus"),
    path("cart/minus/<int:id>/", views.cart_minus, name="cart_minus"),
    
    
    path('store/<int:category_id>/', views.store, name='store_by_category'),
    
    
    path('service/', views.request_service, name='service'),
    # path('reviews/', views.reviews_list, name='reviews_list'),
    path('mechanic-service/', views.mechanic_service, name='mechanic-service'),
    path('mechanic-service-requst/<int:request_id>/', views.mechanic_service_request, name='mechanic-service-requst'),
    path('update_status/<int:request_id>/', views.update_status, name='update_status'),
    
]