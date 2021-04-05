import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ratemyrecipe.settings')

import django
django.setup()

from ratemyrecipeapp.models import Category, Recipe, Rating
from ratemyrecipeapp.models import UserProfile
from django.contrib.auth.models import User

import pandas as pd
from datetime import datetime, timedelta
import random
import os
from ratemyrecipe.settings import MEDIA_DIR

def populate():

    # load the csv with the recipes
    r = pd.read_csv('recipes.tsv', sep='\t')
    
    files = os.listdir(os.path.join(MEDIA_DIR, "category_images/"))

    # add the users
    users = r.added_by.unique()
    for u in users:
        user = add_user(u)
        # get the recipes added by that users
        mask = r['added_by'] == u
        r_user = r[mask].copy()
        # add the categories
        cats = r_user.cat.unique()
        for counter in range(0, len(cats)):
            c = cats[counter]
            for file in files:
                new_file = file.strip('.jpg')
                if new_file == c:
                    picture = "category_images/{0}".format(file)
            
            category = add_category(c, picture)
            # get the recipes in that category
            mask = r_user['cat'] == c
            r_cats = r_user[mask].copy()
            # turn into a dictionary
            recipes = r_cats.set_index('title').T.to_dict()
            # add the recipes
            for r_title, r_info in recipes.items():
                ing = r_info['ingredients']
                dirs = r_info['directions']
                veg = r_info['is_vegan']
                vegt = r_info['is_vegetarian']
                cost = r_info['cost']
                time = r_info['time']

                new_recipe = add_recipe(
                    r_title, category, ing, dirs,
                    veg, vegt, cost, time, user
                )

    #  add the ratings to the recipes
    recipes = Recipe.objects.all()
    users = UserProfile.objects.all()
    for rec in recipes:
        for usr in users:
            title = rec.title
            rated_by = usr.__str__()
            rating = random.randint(1, 5)
            add_rating(title, rated_by, rating)

    # print out the recipes we have added
    print('Recipes added: ')
    for r in Recipe.objects.all():
        print(f'\t- {r}')

    # print out the ratings
    print('Ratings added: ')
    for rating in Rating.objects.all():
        print(f'\t- {rating}')


def add_user(username):
    user = User.objects.create_user(username, password='generic123')
    user.save()
    rmr_user = UserProfile.objects.get_or_create(user=user)[0]
    rmr_user.save()
    return rmr_user


def add_category(cat_name, picture):
    c = Category.objects.get_or_create(name=cat_name, picture=picture)[0]
    c.save()
    return c


def add_recipe(title, cat, ing, dirs, veg, vegt, cost, time, user):
    r = Recipe.objects.get_or_create(
        title=title, category=cat,
        ingredients=ing, directions=dirs, 
        is_vegan=veg, is_vegetarian=vegt,
        cost=cost, time_needed=time,
        added_by=user
    )[0]
    r.save()
    return r
    ...


def add_rating(title, rated_by, rating):
    recipe = Recipe.objects.filter(title=title).first()
    user = User.objects.filter(username=rated_by).first()
    rmr_user = UserProfile.objects.filter(user=user).first()
    r = Rating.objects.get_or_create(
        rating=rating,
        rated_by=rmr_user,
        recipe=recipe
    )[0]
    r.save()
    return r


def parse_time(time_str):
    t = datetime.strptime(time_str, "%H:%M:%S")
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta


if __name__ == '__main__':
    print('Starting RateMyRecipeApp population script...')
    populate()
