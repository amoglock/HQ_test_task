from django.contrib import admin

from products.models import Purchase, Team, Product, Lesson
from products.utils.sort_student import sort_student


class ProductAdmin(admin.ModelAdmin):
    actions = ['redistribute_users_action']  # Добавляем новый action

    def redistribute_users_action(self, request, queryset):
        for product in queryset:
            sort_student(product)

    redistribute_users_action.short_description = "Перераспределить участников в группах"


admin.site.register(Product, ProductAdmin)
admin.site.register(Lesson)
admin.site.register(Purchase)
admin.site.register(Team)
