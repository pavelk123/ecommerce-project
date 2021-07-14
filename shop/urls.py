from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('category/<slug:category_slug>/product/<slug:product_slug>', views.product, name='product_detail'),
	path('category/<slug:category_slug>', views.home, name='cat_page'),
	path('cart/', views.cart_detail, name='cart_detail'),
	path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
	path('cart/remove/<int:product_id>', views.remove_cart, name='remove_cart'),
	path('cart/delete/<int:product_id>', views.remove_cart_product, name='remove_cart_product'),
	path('account/create/', views.signUpView, name="signup"),
	path('account/login', views.loginView, name = 'login'),
	path('account/logout', views.logoutView, name='logout')
]