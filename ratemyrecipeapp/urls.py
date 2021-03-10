from django.urls import path
from ratemyrecipeapp import views

app_name = 'ratemyrecipeapp'

urlpatterns = [
        # If an empty string is provided as the url, this is mapped to the index page
        path('', views.index, name='index'),
        path('categories/', views.categories, name="categories"),
]

