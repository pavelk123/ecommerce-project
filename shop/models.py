from django.db import models
from django.urls import reverse

class Category(models.Model):
	name = models.CharField(max_length=254, unique=True, verbose_name='Название категории')
	slug = models.SlugField(max_length=254, unique=True)
	description = models.TextField(blank=True, verbose_name='Описание Категории')
	image= models.ImageField(upload_to='category',blank=True)


	def __str__(self):
		return self.name

	def get_url(self):
		return reverse('cat_page', args=[self.slug])#name из views

	
	class Meta:
		ordering = ('name',)# Поле по которому сортируются данные
		verbose_name = 'Category'#для правильного отображения во множественном числе
		verbose_name_plural = 'Categories'

class Product(models.Model):
	title = models.CharField(max_length=254, unique=True, verbose_name='Название Продукта')
	slug = models.SlugField(max_length=254, unique=True)
	description = models.TextField(blank=True, verbose_name='Описание Продукта')
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits= 10, decimal_places=2)
	image = models.ImageField(upload_to='product',blank=True)
	stock = models.IntegerField(verbose_name='остаток на складе')
	available = models.BooleanField(default=True,verbose_name='Имеется в наличии')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		 
		return f'{self.category.name} //  {self.title }'


	class Meta:
		ordering = ('title',)
		verbose_name = 'Product'
		verbose_name_plural = 'Products'

	def get_url(self):
		return reverse('product_detail', args=[self.category.slug ,self.slug])#name из urls.py, ссылка на категорию, тк мы указали ее в urls.py

class Cart(models.Model):
	cart_id = models.CharField(max_length=254,blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering= ['date_added',]
		db_table = 'Cart'

	def __str__(self):
		return self.cart_id


class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	quantity= models.IntegerField(default=0)
	models = models.BooleanField(default=True)

	class Meta:
		db_table='CartItem'

	def sub_total(self):
		return self.quantity * int(self.product.price)
	
	def __str__(self):
		return self.product