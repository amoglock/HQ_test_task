from django.urls import path
from .views import ProductListAPIView, LessonListAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:product_id>/lessons/<int:user_id>', LessonListAPIView.as_view(), name='lesson-list'),
]
