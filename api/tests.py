from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from products.models import Product, Purchase, Lesson


class ProductListAPIViewTest(TestCase):
    """
    Тесты API списка продуктов
    """
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем тестовые данные для продуктов
        Product.objects.create(
            creator=self.user, title='Product 1', start_date='2024-03-01', cost=10, max_students=10
        )
        Product.objects.create(
            creator=self.user, title='Product 2', start_date='2024-03-02', cost=15, max_students=8
        )

        # Создаем клиент API
        self.client = APIClient()

    def test_product_list(self):
        # Отправляем GET-запрос к API для получения списка продуктов
        url = '/api/products/'
        response = self.client.get(url)

        # Проверяем, что запрос успешен (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что количество продуктов в ответе соответствует созданным тестовым данным
        self.assertEqual(len(response.data), 2)

        # Дополнительные проверки, например, проверка содержания конкретных полей продукта
        self.assertEqual(response.data[0]['title'], 'Product 1')
        self.assertEqual(response.data[1]['cost'], '15.00')


class LessonListAPIViewTest(TestCase):
    """
    Тесты API списка уроков
    """
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем продукт
        self.product = Product.objects.create(
            creator=self.user, title='Test Product', start_date='2024-03-01', cost=10, max_students=10
        )

        # Создаем уроки
        self.lesson1 = Lesson.objects.create(
            product=self.product, title='Lesson 1', video_link='https://example.com/lesson1'
        )
        self.lesson2 = Lesson.objects.create(
            product=self.product, title='Lesson 2', video_link='https://example.com/lesson2'
        )

        # Пользователь покупает продукт
        self.purchase = Purchase.objects.create(user=self.user, product=self.product)

        # Создаем клиент API
        self.client = APIClient()

    def test_lesson_list_with_access(self):
        """
        Пользователь имеет доступ к продукту
        """

        url = reverse('lesson-list', args=[self.product.id, self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Проверяем количество уроков в ответе

    def test_lesson_list_without_access(self):
        """
        Пользователь не имеет доступ к продукту
        """

        user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        url = reverse('lesson-list', args=[self.product.id, user2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Access to lessons for this product is not allowed.")