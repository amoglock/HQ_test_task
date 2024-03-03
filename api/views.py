from rest_framework import generics, status
from rest_framework.response import Response

from api.serializers import ProductSerializer, LessonSerializer
from products.models import Product, Purchase, Lesson


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        # Получаем id пользователя и id продукта из параметров запроса
        product_id = self.kwargs['product_id']
        user_id = self.kwargs['user_id']

        # Проверяем, имеет ли пользователь доступ к продукту
        if Purchase.objects.filter(user_id=user_id, product_id=product_id).exists():
            # Если доступ есть, возвращаем уроки по конкретному продукту
            return Lesson.objects.filter(product_id=product_id)
        else:
            # Если доступа нет, возвращаем пустой queryset
            return Lesson.objects.none()

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        product_id = self.kwargs['product_id']

        # Проверяем, имеет ли пользователь доступ к продукту
        if Purchase.objects.filter(user_id=user_id, product_id=product_id).exists():
            return super().list(request, *args, **kwargs)
        else:
            # Если доступа нет, возвращаем сообщение об ошибке
            return Response({
                "detail": "Access to lessons for this product is not allowed."
            },
                status=status.HTTP_403_FORBIDDEN
            )
