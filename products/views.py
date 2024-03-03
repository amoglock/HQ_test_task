from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect

from products.models import Product, Purchase, Lesson
from products.utils.add_student import add_student


def home(request):
    """Начальная страница"""

    products = Product.objects.all()
    return render(request, 'products/home.html', context={'products': products})


def purchase_product(request, product_id):
    """Покупка продукта"""

    user = request.user

    product = get_object_or_404(Product, pk=product_id)
    user_purchased = Purchase.objects.filter(user=request.user, product=product).exists()

    if not user_purchased:
        Purchase.objects.create(user=user, product=product)
        add_student(product, request)

    return redirect('view_product', product_id=product_id)


def view_product(request, product_id):
    """Просмотр продукта"""

    product = get_object_or_404(Product, pk=product_id)
    lessons = Lesson.objects.filter(product=product)

    try:
        user_purchased = Purchase.objects.filter(user=request.user, product=product).exists()

        if user_purchased:  # Если продукт куплен
            return render(
                request, 'products/view_product.html', {"product": product, 'lessons': lessons}
            )
        else:
            return render(
                request, 'products/purchase_required.html', {"product": product}
            )
    except Exception as e:  # Обработка ошибки, если пользователь не авторизован
        return render(request, 'products/purchase_required.html', {"product": product})


def register_user(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):

    logout(request)
    return redirect('homepage')
