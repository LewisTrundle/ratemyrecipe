import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ratemyrecipe.settings')

import django
django.setup()

from ratemyrecipeapp.models import Category, Recipe, Rating
from ratemyrecipeapp.models import UserProfile
from django.contrib.auth.models import User

import pandas as pd
from datetime import datetime, timedelta

def populate():

    # load the csv with the recipes
    r = pd.read_csv('recipes.csv')

    # add the users
    users = r.added_by.unique()
    for u in users:
        print(u)
        user = add_user(u)
        # get the recipes added by that users
        mask = r['added_by'] == u
        r_user = r[mask].copy()
        # add the categories
        cats = r_user.cat.unique()
        for c in cats:
            category = add_category(c)
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
                cost = r_info['cost']
                time_str = r_info['time']
                time = parse_time(time_str)

                add_recipe(
                    r_title, category, ing, dirs,
                    veg, cost, time, user
                )

    # print out the recipes we have added
    for r in Recipe.objects.all():
        print(r)


def add_user(username):
    user = User.objects.create_user(username, password='generic123')
    user.save()
    rmr_user = UserProfile.objects.get_or_create(user=user)[0]
    rmr_user.save()
    return rmr_user


def add_category(cat_name):
    c = Category.objects.get_or_create(name=cat_name)[0]
    c.save()
    return c


def add_recipe(title, cat, ing, dirs, veg, cost, time, user):
    r = Recipe.objects.get_or_create(
        title=title, category=cat,
        ingredients=ing, directions=dirs, is_vegan=veg,
        cost=cost, time_needed=time,
        added_by=user
    )[0]
    r.save()
    return r
    ...


def add_rating():
    # add ratings
    ...


def parse_time(time_str):
    t = datetime.strptime(time_str, "%H:%M:%S")
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta

if __name__ == '__main__':
    print('Starting RateMyRecipeApp population script...')
    populate()