from django.contrib import admin
# from django.contrib.auth.models import User
from .models import Products,User
# Register your models here.
admin.site.register(User)
admin.site.register(Products)
