from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Category, Product, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def home(request, category_slug = None):
	products=None
	category_page=None
	if category_slug != None:
		category_page = get_object_or_404(Category, slug = category_slug)
		products = Product.objects.filter(category=category_page, available=True)
	else:
		products = Product.objects.all().filter(available=True)

	return render(request, 'home.html', {'products':products, 'category_page':category_page})



def product(request, category_slug, product_slug):
	
	try:
		product = Product.objects.get(category__slug=category_slug, slug= product_slug)

	except Exception as e:
		raise e

	return render(request, 'product.html',{'product': product})


def _cart_id(request):
	#создаем или получаем сессию
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart


def add_cart(request, product_id):
	product = Product.objects.get(id= product_id)
	#создаем или получаем корзину из бд
	try:
		cart= Cart.objects.get(cart_id=_cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(cart_id=_cart_id(request))
		cart.save()
	#добавление товара в корзину
	try:
		cart_item= CartItem.objects.get(cart= cart, product=product)
		if cart_item.quantity < cart_item.product.stock:
			cart_item.quantity +=1
		cart_item.save()
	
	except CartItem.DoesNotExist:
		cart_item= CartItem.objects.create(cart= cart, product=product, quantity=1)
		cart_item.save()

	return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
	try:
		#получаем карзину и товары в корзине по сессии пользователя
		cart = Cart.objects.get(cart_id = _cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, )
		#счет итоговой стоимости и количества
		for cart_item in cart_items:
			total += cart_item.product.price * cart_item.quantity
			counter += cart_item.quantity 
	except ObjectDoesNotExist:
		pass

	return render(request, 'cart.html', {'cart_items':cart_items,'total':total,'counter': counter})


def remove_cart(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request),)
	product = Product.objects.get(id= product_id) 
	cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()

	return redirect('cart_detail')


def remove_cart_product(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request),)
	product = Product.objects.get(id= product_id) 
	cart_item = CartItem.objects.get(product=product, cart=cart)
	cart_item.delete()
	return redirect('cart_detail')