from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRegisterModel(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	age=models.IntegerField(default=18)
	address=models.TextField(max_length=80)
	mob_no=models.CharField(max_length=10)
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)

	def __str__(self):
		return (self.user.first_name+" "+self.user.last_name)

class eBooksModel(models.Model):
	Image=models.ImageField(upload_to="books/")
	PDF_Files=models.FileField(upload_to="ebooks/")
	Book_Name=models.TextField(max_length=50)
	Author=models.TextField(max_length=50,default='',blank=True)
	Category=models.TextField(max_length=50)
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.Book_Name

class BooksModel(models.Model):
	Image=models.ImageField(upload_to="books/")
	Book_Name=models.TextField(max_length=50)
	Author=models.TextField(max_length=50)
	Price=models.IntegerField(default=100)
	Quantity=models.IntegerField(default=10)
	Language=models.TextField(max_length=50)
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.Book_Name

class AddCartModel(models.Model):
	user=models.CharField(max_length=30,unique=False)
	Book_Name=models.CharField(max_length=50)
	Price=models.IntegerField(default=100)
	payment_status=models.BooleanField(default=False)
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.Book_Name




