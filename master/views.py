from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView, ListView, UpdateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
from master.forms import UserRegisterForm, ExtendedUserForm, eBooksForm, BooksForm
from django.contrib.auth.models import User
from master.models import *
from BookishMai.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.

class HomeView(TemplateView):
	template_name="home.html"

class AdminView(TemplateView):
	template_name="dashbord.html"

class UserView(View):
	template_name="userhome.html"

	def get(self,request):
		cur_user=int(request.user.id)-1
		context={
		'userbooks':BooksModel.objects.all(),
		'cart_count':AddCartModel.objects.filter(user=cur_user,payment_status=False).count()
		}

		return render(request,self.template_name,context)

class AboutUsView(TemplateView):
	template_name="about.html"

class UserAboutUsView(TemplateView):
	template_name="userabout.html"

class SecureShoppingView(TemplateView):
	template_name="secureshopping.html"

class UserSecureShoppingView(TemplateView):
	template_name="usersecureshopping.html"

class PrivacyView(TemplateView):
	template_name="privacy.html"

class UserPrivacyView(TemplateView):
	template_name="userprivacy.html"

class PaymentShowView(TemplateView):
	template_name="payment_options.html"

class UserPaymentView(TemplateView):
	template_name="userpayment.html"

class ContactView(TemplateView):
	template_name="contact.html"

class UserContactView(TemplateView):
	template_name="usercontact.html"

def adduser(request):
	if request.method=="POST":
		form=UserRegisterForm(request.POST)
		extend_form=ExtendedUserForm(request.POST,request.FILES)

		if form.is_valid() and extend_form.is_valid():
			user=form.save()
			extended_profile=extend_form.save(commit=False)
			extended_profile.user=user
			extended_profile.save()

			sub = forms.UserRegisterForm(request.POST)
			fname = str(sub['first_name'].value())
			lname = str(sub['last_name'].value())
			subject = 'Welcome to BookishMai'
			message = 'Hi %s %s, Your registration with BookishMai was successful. Now you can use the credentials to login.  Hope you are enjoying your Day' %(fname,lname)
			recepient = str(sub['email'].value())
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently =False)

			username_var=form.cleaned_data.get('username')
			password_var=form.cleaned_data.get('password1')
			user=authenticate(username=username_var,password=password_var)

			login(request,user)
			return redirect ('userhome')
	else:
		form=UserRegisterForm(request.POST)
		extend_form=ExtendedUserForm(request.POST,request.FILES)

	context={"form":form,"extend_form":extend_form}
	return render(request,'adduser.html',context)

class UserLogin(View):
	def get(self,request):
		form=AuthenticationForm()
		context={'form':form}
		return render(request,'login1.html',context)

	def post(self,request):
		username=request.POST.get('username')
		password=request.POST.get('password')
		recaptcha_response = request.POST.get('g-recaptcha-response')
		data = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response
		}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
		result = r.json()

		if result['success']:
			user=authenticate(username=username,password=password)
			login(request,user,backend='django.contrib.auth.backends.ModelBackend')
		
			if user is not None :
				login(request,user)
				if user.is_superuser == True and user.is_staff == True:
					return redirect('adminhome')
				if user.is_staff == True and user.is_superuser == False:
					return redirect('staffview')
				if user.is_staff == False and user.is_superuser == False:
					return redirect ('userhome')
			else:
				form=AuthenticationForm()
				context={'form':form}
				return render(request,'login1.html',context)


class BooksView(CreateView):
	template_name='addbook.html'
	form_class=BooksForm
	success_url='/add/book/'

class eBooksView(CreateView):
	template_name='addebook.html'
	form_class=eBooksForm
	success_url='/add/ebook/'

# for User e-Books List
class UsereBooksList(ListView):
	template_name="userebooklist.html"
	model=eBooksModel
	context_object_name='ebooks'
	paginate_by = 10

# for Admin e-Books List
class AdmineBooksList(ListView):
	template_name="ebooklist.html"
	model=eBooksModel
	context_object_name='adminebooks'
	paginate_by = 10

class eBookEditView(UpdateView):
	template_name="ebookedit.html"
	model=eBooksModel
	fields=['Image','PDF_Files','Book_Name','Author','Category']
	success_url='/list/ebooks/'

# for Admin Books List
class BooksList(ListView):
	template_name="booklist.html"
	model=BooksModel
	context_object_name='books'
	paginate_by = 10

# for User Books List
class UserBooksList(View):
	template_name="userbooklist.html"
	
	def get(self,request):
		cur_user=int(request.user.id)-1
		context={
		'userbooks':BooksModel.objects.all(),
		'cart_count':AddCartModel.objects.filter(user=cur_user,payment_status=False).count()
		}

		return render(request,self.template_name,context)

class BookDetailsView(DetailView):
	template_name="bookdetails.html"
	model=BooksModel
	
class BookEditView(UpdateView):
	template_name="bookedit.html"
	model=BooksModel
	fields=['Image','Book_Name','Author','Price','Quantity','Language']
	success_url='/list/books/'

class BookRemoveView(View):
	def get(self,request,pk):
		BooksModel.objects.get(id=pk).delete()
		return redirect('listbook')

def logout_request(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("home")

class AddCartView(View):
	def get(self,request,pk):
		data=BooksModel.objects.get(id=pk)
		# print("DATA: ",data)
		cur_user=UserRegisterModel.objects.get(user=request.user)
		Name_var=data.Book_Name
		Price_var=data.Price
		print(cur_user)
		print(Name_var)
		print(Price_var)

		AddCartModel.objects.create(
			user=cur_user.id,
			Book_Name=Name_var,
			Price=Price_var
			)
		return redirect('userlistbook')

class ListCartView(View):
	template_name='cartlist.html'

	def get(self,request):
		cur_user=int(request.user.id)-1
		print("cur_user",cur_user)
		
		context={

		'cart_list':AddCartModel.objects.filter(user=cur_user,payment_status=False),
		'total_price':AddCartModel.objects.filter(user=cur_user,payment_status=False).aggregate(Sum('Price'))['Price__sum'],
		}
		return render(request,self.template_name,context)

class OrderHistoryView(View):
	template_name='orderhistory.html'

	def get(self,request):
		cur_user=int(request.user.id)-1
		context={
		'order_list':AddCartModel.objects.filter(user=cur_user,payment_status=True)
		}
		return render(request,self.template_name,context)

class CartRemoveView(View):
	def get(self,request,pk):
		AddCartModel.objects.get(id=pk).delete()
		return redirect('usercartlist')

class UserDetailsView(View):
	template_name="userdetails.html"
	model=UserRegisterModel
	def get(self,request, pk):
		user = self.model.objects.get(id=int(pk))
		context = {
		'cuser' : user
		}
		return render(request, self.template_name, context)


class OrderList(View):
	template_name='orderlist.html'

	def get(self,request):
		context={
		'user_order':AddCartModel.objects.filter(payment_status=True)
		}
		return render(request,self.template_name,context)

#resetpassword...........................................................

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "Password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})


#payment.............................................................

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

class PaymentView(View):
	template_name="payment.html"

	def get(self,request):
		cur_user=int(request.user.id)-1
		data=AddCartModel.objects.filter(user=cur_user,payment_status=False).aggregate(Sum('Price'))['Price__sum']
		amount=int(data)*100
		currency = 'INR'
		# amount = 20000  # Rs. 200
 
		# Create a Razorpay Order
		razorpay_order = razorpay_client.order.create(dict(amount=amount,
			currency=currency,payment_capture='0'))
 
		# order id of newly created order.
		razorpay_order_id = razorpay_order['id']
		callback_url = '/paymenthandler/'
 
		# we need to pass these details to frontend.
		context = {'amount_rupee':data}
		context['razorpay_order_id'] = razorpay_order_id
		context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
		context['razorpay_amount'] = amount
		context['currency'] = currency
		context['callback_url'] = callback_url
 
		return render(request,self.template_name, context=context)

 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
	# only accept POST request.
	if request.method == "POST":
		try:
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}
		
			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
				# amount = 20000  # Rs. 200
				cur_user=int(request.user.id)-1
				data=AddCartModel.objects.filter(user=cur_user,payment_status=False).aggregate(Sum('Price'))['Price__sum']
				amount=int(data)*100

				try:
 
					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)
					data=AddCartModel.objects.filter(user=cur_user,payment_status=False)
					for i in data:
						book_name=i.Book_Name
						book_data=BooksModel.objects.get(Book_Name=book_name)
						print(book_data)
						book_data.Quantity=book_data.Quantity-1
						book_data.save()
						i.payment_status=True
						i.save()
 
					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:
 
					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:
 
				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:
 
			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
		# if other than POST request is made.
		return HttpResponseBadRequest()
				
		