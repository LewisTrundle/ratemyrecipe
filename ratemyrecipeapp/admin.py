from django.contrib import admin
from ratemyrecipeapp.models import Category, Recipe
from ratemyrecipeapp.models import UserProfile

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(UserProfile)
