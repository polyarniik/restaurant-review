from django.contrib import admin

# Register your models here.
from account.forms import User

admin.site.register(User)
