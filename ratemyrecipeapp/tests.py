from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category
from .models import Recipe, Rating
from .models import UserProfile


def create_category():
    c = Category.objects.create(name='test category')
    return c


def create_user():
    u = User.objects.create(username='test-user', password='testing1234')
    usr = UserProfile.objects.create(user=u)
    return usr


def create_recipe(title, usr, cat):
    rec = Recipe.objects.create(
        title=title, category=cat, added_by=usr,
        is_vegan=False, is_vegetarian=True, cost=10,
        time_needed='01:30'
    )
    return rec


class RecipeMethodTests(TestCase):
    def test_ensure_cost_is_nonnegative(self):
        cat = create_category()
        usr = create_user()

        rec = Recipe(
            title='test recipe', category=cat, added_by=usr,
            is_vegan=False, is_vegetarian=True
        )
        rec.cost = -10
        rec.save()

        self.assertEqual((rec.cost >= 0), True)


class RatingMethodTests(TestCase):
    def test_ensure_rating_is_less_than_5(self):
        usr = create_user()
        cat = create_category()
        rec = create_recipe('test recipe 1', usr, cat)

        r = Rating.objects.create(
            recipe=rec, rated_by=usr, rating=8
        )

        self.assertEqual((r.rating <= 5), True)

    def test_ensure_rating_is_greater_than_1(self):
        usr = create_user()
        cat = create_category()
        rec = create_recipe('test recipe 1', usr, cat)

        r = Rating.objects.create(
            recipe=rec, rated_by=usr, rating=-4
        )

        self.assertEqual((r.rating >= 1), True)
