from django.urls import path
from ratemyrecipeapp import views

app_name = 'ratemyrecipeapp'

urlpatterns = [
        # If an empty string is provided as the url, this is mapped to the index page
        path('', views.index, name='index'),
        
        path('categories/', views.categories, name="categories"),
        path('chosen_category/<slug:category_name_slug>/', views.chosen_category, name="chosen_category"),
        path('chosen_recipe/<slug:recipe_name_slug>/', views.chosen_recipe, name="chosen_recipe"),
        path('trending/', views.trending, name="trending"),
        path('signUp/', views.sign_up, name="signUp"),
        path('login/', views.user_login, name="login"),
        path('logout/', views.user_logout, name='logout'),
        path('account/', views.my_account, name="account"),
]

