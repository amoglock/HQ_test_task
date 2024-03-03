from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from products.models import Product, Purchase, Lesson


class ProductsViewsTestCase(TestCase):

    def setUp(self):

        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем продукт
        self.product = Product.objects.create(
            title='Test Product',
            creator=self.user,
            start_date=timezone.now(),
            cost=10.0
        )

        # URL-адреса
        self.home_url = reverse('homepage')
        self.purchase_url = reverse('purchase_product', args=[self.product.id])
        self.view_product_url = reverse('view_product', args=[self.product.id])

    def test_home_view(self):

        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/home.html')

    def test_purchase_product_view_authenticated_user(self):

        # Аутентифицируем пользователя
        self.client.force_login(self.user)

        response = self.client.get(self.purchase_url)
        self.assertEqual(response.status_code, 302)  # Должно перенаправить на страницу просмотра продукта

        # Проверяем, что пользователь купил продукт
        self.assertTrue(Purchase.objects.filter(user=self.user, product=self.product).exists())

    # def test_purchase_product_view_unauthenticated_user(self):
    #
    #     response = self.client.get(self.purchase_url)
    #     self.assertEqual(response.status_code, 302)  # Должно перенаправить на страницу входа

    def test_view_product_authenticated_user(self):

        # Аутентифицируем пользователя
        self.client.force_login(self.user)

        # Покупаем продукт
        Purchase.objects.create(user=self.user, product=self.product)

        response = self.client.get(self.view_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/view_product.html')

    def test_view_product_unauthenticated_user(self):

        response = self.client.get(self.view_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/purchase_required.html')
