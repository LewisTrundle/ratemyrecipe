from django.shortcuts import render
from django.http import HttpResponse
from ratemyrecipeapp.models import Category, Recipe, Rating
from math import random

def index(request):
    
    # Gets a list of every recipe
    recipes = list(Recipe.objects.all())
    # Picks a random recipe
    ran_recipe = random.sample(recipes, 1)
    
    rating = Rating.objects.filter(recipe=ran_recipe)
    
    
    
    context_dict = {}
    context_dict['welcome'] = "Welcome to Rate My Recipe!"
    context_dict['ran_recipe'] = ran_recipe
    context_dict['rating'] = rating
    
    return render(request, 'rango/index.html', context=context_dict)



def categories(request):
    return HttpResponse("This is the categories page")


def trending(request):
    pass

def sign_up(request):
    pass

def login(request):
    pass

def my_account(request):
    pass

def my_recipes(request):
    pass

def recipes_ive_rated(request):
    pass

