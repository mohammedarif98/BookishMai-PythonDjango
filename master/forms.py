from django import forms
from master.models import UserRegisterModel,BooksModel, eBooksModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	class Meta:
		model=User
		fields=["username","first_name","last_name","password1","password2","email"]

class ExtendedUserForm(forms.ModelForm):
	class Meta:
		model=UserRegisterModel
		fields=["age","address","mob_no"]

class eBooksForm(forms.ModelForm):
	class Meta:
		model=eBooksModel
		exclude=('status','created_on')

class BooksForm(forms.ModelForm):
	class Meta:
		model=BooksModel
		exclude=('status','created_on')

class Subscribe(forms.Form):
	Email = forms.EmailField()
	def __str__(self):
		return self.Email