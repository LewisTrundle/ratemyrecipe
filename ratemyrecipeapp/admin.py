from django.contrib import admin
from ratemyrecipeapp.models import Category, Recipe, Rating
from ratemyrecipeapp.models import UserProfile

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Rating)
admin.site.register(UserProfile)
