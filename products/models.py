from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):

    creator: User = models.ForeignKey(User, verbose_name="who created", on_delete=models.CASCADE)
    title: str = models.CharField("product name", max_length=128)
    start_date = models.DateField("product start date", null=True)
    cost: float = models.DecimalField("cost of product", max_digits=7, decimal_places=2)
    min_students: int = models.PositiveIntegerField("minimal number users in group", default=5)
    max_students: int = models.PositiveIntegerField("maximal number users in group", default=10)

    def __str__(self) -> str:
        return self.title


class Purchase(models.Model):

    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - {self.purchase_date_time}"

    class Meta:
        unique_together = ['user', 'product']  # Пользователь может купить продукт только один раз


class Lesson(models.Model):

    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_link = models.URLField()

    def __str__(self):
        return self.title


class Team(models.Model):

    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField("group name", max_length=50)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.product} - {self.title}'
