from django.contrib import admin

from .models import UserRegister
# Register your models here.

admin.site.register(UserRegister)
admin.site.site_header = "Meeting On Cloud Admin"



