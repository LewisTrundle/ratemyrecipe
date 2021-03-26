from django.urls import path
from ratemyrecipeapp import views

app_name = 'ratemyrecipeapp'

urlpatterns = [
        # If an empty string is provided as the url, this is mapped to the index page
        path('', views.index, name='index'),
        
        path('categories/', views.categories, name="categories"),
        path('categories/<slug:category_name_slug>/', views.categories, name="chosen_category"),
        path('trending/', views.trending, name="trending"),
        path('signup/', views.sign_up, name="signUp"),
        path('login/', views.login, name="login"),
        path('logout/', views.logout, name='logout'),
        path('account/', views.my_account, name="account"),
]

