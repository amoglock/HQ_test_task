from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('purchase/<int:product_id>/', views.purchase_product, name='purchase_product'),
    path('product_details/<int:product_id>/', views.view_product, name='view_product'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
