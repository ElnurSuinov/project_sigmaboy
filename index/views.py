from django.shortcuts import render, redirect, get_object_or_404

from .bot import send_order_to_tg
from .models import Category, Product, Cart
from .forms import RegForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View
import telebot

bot = telebot.TeleBot(token="TOKEN")
chat_id = 'CHAT_ID'

# Create your views here.
# Главная страница
def home_page(request):
    # Достаём всё из БД
    categories = Category.objects.all()
    products = Product.objects.all()
    # Передаём данные на Frontend
    context = {
        'categories': categories,
        'products': products
        }
    return render(request, 'home.html', context)

# Страница выбранной категории
def category_page(request, pk):
    # Достаём данные из БД
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(product_category=category)
    # Передаём данные на Frontend
    context = {
        'category': category,
        'products': products
    }
    return render(request,'category.html', context)

# Страница выбранного товара
def product_page(request, pk):
    # Достаём данные из БД
    product = Product.objects.get(id=pk)
    # Передаём данные из Frontend
    context = {'product': product}
    return render(request, 'product.html', context)

# Поиск товара по названию
def search(request):
    if request.method == 'POST':
        # Достаём данные с формы
        get_product = request.POST.get('search_product')
        # Достаём данные из БД
        searched_product = Product.objects.filter(product_name__iregex=get_product)
        if searched_product:
            context = {
                'products': searched_product,
                'request': get_product
            }
            return render(request, 'result.html', context)
        else:
            context = {
                'products': "",
                'request': get_product
            }
            return render(request, 'result.html', context)


# Регистрация
class Register(View):
    template_file = 'registration/register.html'

    def get(self, request):
        context = {'form': RegForm}
        return render(request, self.template_file, context)

    def post(self, request):
        form = RegForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')

            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            login(request, user)
            return redirect('/')


# Выход из аккаунта
def logout_view(request):
    logout(request)
    return redirect('/')


# Добавление товара в корзину
def add_to_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        user_count = int(request.POST.get('pr_amount'))
        if 1 <= user_count <=product.product_count:
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_pr_amount=user_count).save()
            return redirect('/')
    return redirect(f'/product/{pk}')


# Отображение корзины
def cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)
    context = {'cart': user_cart}
    return render(request, 'cart.html', context)

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('cart_view')

def checkout(request):
    user_id = request.user.id
    cart = Cart.objects.filter(user_id=user_id)

    if not cart.exists():
        return redirect('cart_view')

    if request.method == "POST":
        for item in cart:
            if item.user_pr_amount > item.user_product.product_count:
                context = {
                    "cart_items": cart,
                    "total_count": sum(item.user_product.product_price * item.user_pr_amount for item in cart),
                    "error": f"Товар {item.user_product.product_name} который вы хотите заказать в таком количестве"
                }
                return render(request, 'checkout.html', context=context)

        for item in cart:
            item.user_product.product_count -= item.user_pr_amount
            item.user_product.save()

        message_lines = [f"Новый заказ <b>\n От пользователя ID {user_id} </b>\n"]
        for i in cart:
            message_lines.append(
                f"{i.user_product.product_name} x {i.user_pr_amount}"
                f"= {i.user_product.product_price * i.user_pr_amount}"
            )
        total_price = sum(item.user_product.product_price * item.user_pr_amount for item in cart)
        message_lines.append(f"\n Итого вышло: {total_price}")

        send_order_to_tg("\n".join(message_lines))
        cart.delete()
        return redirect("home")
    total_price = sum(item.user_product.product_price * item.user_pr_amount for item in cart)
    return render(request, "checkout.html", context={
        "cart": cart,
        "total_price": total_price
    })

