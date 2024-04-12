from django.contrib import admin
from .models import CustomUser, RefreshToken
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(RefreshToken)		
