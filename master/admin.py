from django.contrib import admin
from master.models import *

# Register your models here.

admin.site.register(UserRegisterModel)
admin.site.register(BooksModel)
admin.site.register(eBooksModel)
admin.site.register(AddCartModel)