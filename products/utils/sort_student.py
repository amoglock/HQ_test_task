from itertools import cycle

from django.contrib.auth.models import User
from django.utils import timezone

from products.models import Team


def sort_student(product):
    """Равномерное распределение участников в группах"""

    if product.start_date <= timezone.now().date():
        return "Перераспределение участников невозможно, так как продукт уже начался."

    # Получаем все группы для продукта
    teams = Team.objects.filter(product=product)

    # Получаем минимальное количество участников в группе
    min_users_in_group = product.min_students

    # Получаем всех участников, отсортированных по дате покупки
    students = User.objects.filter(purchase__product=product).order_by('purchase__purchase_date_time')

    # Сбрасываем принадлежность участников к группам
    for team in teams:
        team.users.clear()

    # Создаем циклический итератор по группам
    group_cycle = cycle(teams)

    # Заполняем группы минимально требуемым количеством участников
    for i in range(min_users_in_group):
        for team in teams:
            student = students.first()
            if student:
                team.users.add(student)
                students = students.exclude(pk=student.pk)

    # Распределяем оставшихся участников равномерно
    for student in students:
        team = next(group_cycle)
        team.users.add(student)

    return "Перераспределение участников успешно завершено."
