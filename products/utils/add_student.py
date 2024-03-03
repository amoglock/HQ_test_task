from products.models import Team


def add_student(product, request):
    """Добавление студента в группу после покупки продукта"""

    group, created = Team.objects.get_or_create(product=product, defaults={'title': f'Group for {product.title}'})

    if group.users.count() < product.max_students:
        group.users.add(request.user)
    else:
        new_group = Team.objects.create(product=product, defaults={'title': f'Group for {product.title}'})
        new_group.users.add(request.user)
        