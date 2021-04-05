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


class RecipeFormTests(TestCase):
    def test_ensure_the_time_format_is_correct(self):
        # if the user does not enter an appropriate time format, print an error message
        pass


class IndexViewTests(TestCase):
    def test_index_view_with_no_recipes(self):
        # display an appropriate message if there are no recipes
        pass

    def test_index_view_with_one_recipe(self):
        # if there is only one recipe, this should be the only recipe shown in the index view
        pass


class CategoriesViewTests(TestCase):
    def test_categories_view_with_no_categories(self):
        # display an appropriate message if there are no categories
        pass

    def test_categories_view_with_categories(self):
        # make sure that all the categories created are displayed in the categories view
        pass

    def test_categories_view_with_authenticated_users_allows_to_add_a_recipe(self):
        # if the user has logged in, then the button says 'add recipe'
        pass

    def test_categories_view_with_non_authenticated_users_ask_for_log_in(self):
        # if the user has not logged in, the button says 'log in'
        pass


class ChosenCategoryViewTests(TestCase):
    def test_chosen_category_view_with_no_recipes(self):
        # if there are no recipe in the current category, display an appropriate error message
        pass

    def test_chosen_catgory_with_recipes(self):
        # all the recipes in a certain category must appear
        pass


class TrendingViewTests(TestCase):
    def test_trending_view_with_no_recipes(self):
        # if there are no recipes, show an appropriate message
        pass

    def test_treding_view_with_one_recipe(self):
        # if there is only one recipe, this should be the only recipe shown in trending
        pass


class AddRecipeViewTests(TestCase):
    def test_add_recipe_view_only_works_with_authenticated_users(self):
        # if a user has not logged in then redirect to the login page
        pass


class MyAcountViewTests(TestCase):
    def test_my_account_view_with_non_authenticated_user_asks_for_log_in(self):
        # if the user has not logged in, then ask for log in/sign up
        pass

    def test_my_account_view_with_authenticated_user_shows_recipes_added_and_rated(self):
        # if the user has logged in, show links to the recipes ive rated and my recipes pages
        pass

# test recipes ive rated and my recipes too!
