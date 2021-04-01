from django.contrib import admin
from ratemyrecipeapp.models import Category, Recipe, Rating
from ratemyrecipeapp.models import UserProfile


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating)
admin.site.register(UserProfile)
