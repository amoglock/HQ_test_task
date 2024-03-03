from django.contrib.auth import get_user_model
from rest_framework import serializers
from products.models import Product, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'video_link']


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    groups_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'start_date', 'cost', 'lessons_count', 'students_count', 'groups_fill_percentage', 'purchase_percentage']

    def get_lessons_count(self, obj):
        """Получаем количество уроков"""
        return obj.lesson_set.count()

    def get_students_count(self, obj):
        """Получаем количество студентов, купивших продукт"""
        return obj.purchase_set.count()

    def get_groups_fill_percentage(self, obj):
        """Процент заполненности групп"""
        max_students_per_group = obj.max_students

        if max_students_per_group == 0:
            return 0

        total_students = obj.purchase_set.count()
        total_groups = (total_students + max_students_per_group - 1) // max_students_per_group

        if total_groups == 0:
            return 0

        average_students_per_group = total_students / total_groups
        fill_percentage = (average_students_per_group / max_students_per_group) * 100
        return round(fill_percentage, 2)

    def get_purchase_percentage(self, obj):
        """Процент приобретения продукта"""
        total_users = get_user_model().objects.count()

        if total_users == 0:
            return 0

        purchased_users = obj.purchase_set.count()
        percentage = (purchased_users / total_users) * 100
        return round(percentage, 2)
