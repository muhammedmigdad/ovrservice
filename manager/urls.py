from django.urls import path
from manager import views

app_name = "manager"

urlpatterns = [
    
   path("", views.index, name="index"),
   path("login/", views.login, name="login"),
   path("logout/", views.logout, name="logout"),
   path("service_request/", views.service_request, name="service_request"),
   path("service_request/add", views.service_request_add, name="service_request_add"),
   path("service_request_edit/<int:id>/", views.service_request_edit, name="service_request_edit"),
   path("service_request_delete/<int:id>/", views.service_request_delete, name="service_request_delete"),
   path("store/", views.store, name="store"),
   path("store_add", views.store_add, name="store_add"),
   path("store_edit/<int:id>/", views.store_edit, name="store_edit"),
   path("store_delete/<int:id>/", views.store_delete, name="store_delete"),
   path("products/", views.products, name="products"),
   path("products_add/", views.products_add, name="products_add"),
   path("products_edit/<int:id>/", views.products_edit, name="products_edit"),
   path("products_delete/<int:id>/", views.products_delete, name="products_delete"),
   path("order/", views.order, name="order"),
   path("users/", views.users, name="users"),
   path("users_delete/<int:id>/", views.users_delete, name="users_delete"),
   path("users_edit/<int:id>/", views.users_edit, name="users_edit"),
   path("users_add/", views.users_add, name="users_add"), 
   path("service/", views.service, name="service"),
   path("service_add", views.service_add, name="service_add"),
   path("service_edit/<int:id>/", views.service_edit, name="service_edit"),
   path("service_delete/<int:id>/", views.service_delete, name="service_delete"),
   path("review/", views.review, name="review"),
   path("review_add", views.review_add, name="review_add"),
   path("review_edit/<int:id>/", views.review_edit, name="review_edit"),
   path("review_delete/<int:id>/", views.review_delete, name="review_delete"),
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   

   
   
   
   
   
]