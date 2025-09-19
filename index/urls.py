from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home"),
    path('category/<int:pk>', views.category_page),
    path('product/<int:pk>', views.product_page),
    path('search', views.search),
    path('register', views.Register.as_view()),
    path('logout', views.logout_view),
    path('add-to-cart/<int:pk>', views.add_to_cart),
    path('cart', views.cart, name="cart_view"),
    path('cart/remove/<int:cart_id>', views.remove_from_cart, name='remove_from_cart'),
    path('checkout', views.checkout, name="checkout_view")
]