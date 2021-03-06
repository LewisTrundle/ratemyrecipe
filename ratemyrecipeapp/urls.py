from django.urls import path
from ratemyrecipeapp import views

app_name = 'ratemyrecipeapp'

urlpatterns = [
        # If an empty string is provided as the url, this is mapped to the index page
        path('', views.index, name='index'),
        
        # URL for categories page
        path('categories/', views.categories, name="categories"),
        # URL for chosen_category page - is working fine
        path('categories/<slug:category_name_slug>/', views.chosen_category, name="chosen_category"),
        
        
        path('random_recipe/<slug:recipe_name_slug>/', views.random_recipe, name="random_recipe"),
        path('chosen_recipe/<slug:recipe_name_slug>/', views.chosen_recipe, name="chosen_recipe"),
        path('categories/<slug:category_name_slug>/<slug:recipe_name_slug>/', views.chosen_recipe, name="chosen_recipe"),
        
        
        path('trending/', views.trending, name="trending"),
        path('signUp/', views.sign_up, name="signUp"),
        path('login/', views.user_login, name="login"),
        path('logout/', views.user_logout, name='logout'),
        path('account/', views.my_account, name="account"),
        path('add_recipe/<slug:category_name_slug>/', views.add_recipe, name='add_recipe'),
        path('my_recipes/', views.my_recipes, name='my_recipes'),
        path('account/recipes_ive_rated/', views.recipes_ive_rated, name='recipes_ive_rated'),
        
        
        path('rate/', views.rate_recipe, name='rate-view'),
]


