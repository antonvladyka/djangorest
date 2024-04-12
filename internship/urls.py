"""internship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from theapp.views import register, login, logout, refresh, me


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/api/register')), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'),
    path('api/refresh/', refresh, name='refresh'),
    path('api/logout/', logout, name='logout'),
    path('api/me/', me, name='me'),
    
]
