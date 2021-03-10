"""ratemyrecipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from ratemyrecipeapp import views

urlpatterns = [
    # If an empty string is entered after the server name, then the user is mapped to the index (home) page
    path('', views.index, name="index"),
    
    # This maps any URL beginning with 'ratemyrecipe/' to be handled by the ratemyrecipeapp urls
    path('ratemyrecipe/', include('ratemyrecipeapp.urls')),
    
    # This is the url mapping for the admin page
    path('admin/', admin.site.urls),
]
