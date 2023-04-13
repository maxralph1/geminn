from django.contrib import admin

from .models import UserModel, Address

admin.site.register(UserModel)
admin.site.register(Address)
