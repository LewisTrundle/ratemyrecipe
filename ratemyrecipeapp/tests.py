from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category
from .models import Recipe, Rating
from .models import UserProfile
from .forms import RecipeForm


def create_category(name):
    c = Category.objects.create(name=name)
    return c


def create_user():
    # u = User.objects.create(username='test-user', password='testing1234')
    usr = UserProfile.objects.create(user=create_django_user())
    return usr


def create_django_user():
    u = User.objects.create(username='test-user', password='testing1234')
    return u


def create_recipe(title, usr, cat):
    rec = Recipe.objects.create(
        title=title, category=cat, added_by=usr,
        is_vegan=False, is_vegetarian=True, cost=10,
        time_needed='01:30'
    )
    return rec


def create_recipe_2(title):
    cat = create_category('test category')
    usr = create_user()
    rec = create_recipe(title, usr, cat)

    return rec


class RecipeMethodTests(TestCase):
    def test_ensure_cost_is_nonnegative(self):
        '''
        If the cost is negative, then set to 0
        '''
        cat = create_category('test category')
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
        ''' 
        If a rating is greater than 5, then change it back to 5
        '''
        usr = create_user()
        cat = create_category('test category')
        rec = create_recipe('test recipe 1', usr, cat)

        r = Rating.objects.create(
            recipe=rec, rated_by=usr, rating=8
        )

        self.assertEqual((r.rating <= 5), True)

    def test_ensure_rating_is_greater_than_1(self):
        '''
        If a rating is less than 1, then change it back to 1
        '''
        usr = create_user()
        cat = create_category('test category')
        rec = create_recipe('test recipe 1', usr, cat)

        r = Rating.objects.create(
            recipe=rec, rated_by=usr, rating=-4
        )

        self.assertEqual((r.rating >= 1), True)


class RecipeFormTests(TestCase):
    def test_recipe_form_time_needed_without_colon(self):
        '''
        if the user does not enter an appropriate time format, print an error message
        '''
        form = RecipeForm(data={'time_needed': '30'})
        self.assertEqual(
            form.errors['time_needed'],
            [RecipeForm.error_message]
        )

    def test_recipe_form_time_needed_shorter_than_expected(self):
        '''
        if the user does not enter an appropriate time format, print an error message
        '''
        form = RecipeForm(data={'time_needed': '2:30'})
        self.assertEqual(
            form.errors['time_needed'],
            [RecipeForm.error_message]
        )


class IndexViewTests(TestCase):
    def test_index_view_with_no_recipes(self):
        '''
        Display an appropriate message if there are no recipes
        '''
        response = self.client.get(reverse('ratemyrecipeapp:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Sorry, there are no recipes available now.')
        self.assertEqual(response.context['Recipe'], None)

    def test_index_view_with_one_recipe(self):
        '''
        If there is only one recipe, this should be the only recipe shown in the index view
        '''
        recipe = create_recipe_2('First recipe')

        response = self.client.get(reverse('ratemyrecipeapp:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'First recipe'
        )
        self.assertEqual(response.context['Recipe'], recipe)


class CategoriesViewTests(TestCase):
    def test_categories_view_with_no_categories(self):
        '''
        Display an appropriate message if there are no categories
        '''
        response = self.client.get(reverse('ratemyrecipeapp:categories'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,  'Sorry, there are no categories available now.'
        )
        self.assertEqual(response.context['categories'], [])

    def test_categories_view_with_categories(self):
        '''
        Make sure that all the categories created are displayed in the categories view
        '''
        c1 = create_category('Asian')
        c2 = create_category("British")
        c3 = create_category('Other')

        response = self.client.get(reverse('ratemyrecipeapp:categories'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Asian')
        self.assertContains(response, 'British')
        self.assertContains(response, 'Other')

        cats_in_view = len(response.context['categories'])
        self.assertEqual(cats_in_view, 3)


class ChosenCategoryViewTests(TestCase):
    def test_chosen_category_view_with_no_recipes(self):
        '''
        If there are no recipe in the current category, display an appropriate error message
        '''
        c = create_category('Asian')

        response = self.client.get(
            reverse('ratemyrecipeapp:chosen_category', args=[c.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'There are no recipes in this category yet.'
        )
        self.assertEqual(response.context['recipes'].count(), 0)

    def test_chosen_category_with_recipes(self):
        '''
        All the recipes in a certain category must appear
        '''
        cat = create_category('Asian')
        usr = create_user()

        r1 = create_recipe('Egg Fried Noodles', usr, cat)
        r2 = create_recipe('Spring Rolls', usr, cat)
        r3 = create_recipe('Korean Fried Chicken', usr, cat)

        response = self.client.get(
            reverse('ratemyrecipeapp:chosen_category', args=[cat.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Egg Fried Noodles')
        self.assertContains(response, 'Spring Rolls')
        self.assertContains(response, 'Korean Fried Chicken')

        recps_in_view = len(response.context['recipes'])
        self.assertEqual(recps_in_view, 3)

    def test_chosen_category_view_with_authenticated_users_allows_to_add_a_recipe(self):
        '''
        If the user has logged in, then the button says 'add recipe'
        '''
        cat = create_category('British')
        usr = create_django_user()

        self.client.force_login(usr)

        response = self.client.get(
            reverse('ratemyrecipeapp:chosen_category', args=[cat.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Add a recipe to {cat.name}')

    def test_chosen_category_view_with_non_authenticated_users_ask_for_log_in(self):
        '''
        If the user has not logged in, the button says 'log in'
        '''
        cat = create_category('British')

        response = self.client.get(
            reverse('ratemyrecipeapp:chosen_category', args=[cat.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Log in to add a recipe to {cat.name}')


class TrendingViewTests(TestCase):
    def test_trending_view_with_no_recipes(self):
        '''
        If there are no recipes, show an appropriate message
        '''
        response = self.client.get(reverse('ratemyrecipeapp:trending'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Sorry, there are no recipes available now.'
        )
        self.assertEqual(response.context['ratings'], [])

    def test_trending_view_with_one_recipe(self):
        '''
        If there is only one recipe, this should be the only recipe shown in trending
        '''
        rec = create_recipe_2('Chocolate Cake')
        u = User.objects.create(username='user1', password='unique123')
        usr = UserProfile.objects.create(user=u)
        rating = Rating.objects.create(
            recipe=rec, rated_by=usr, rating=3
        )

        response = self.client.get(reverse('ratemyrecipeapp:trending'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Trending right now: Chocolate Cake')

        recps_in_view = len(response.context['ratings'])

        self.assertEqual(recps_in_view, 1)


class AddRecipeViewTests(TestCase):
    def test_add_recipe_view_only_works_with_authenticated_users(self):
        '''
        If a user has not logged in then redirect to the login page
        '''
        pass


class MyAcountViewTests(TestCase):
    def test_my_account_view_with_non_authenticated_user_asks_for_log_in(self):
        '''
        If the user has not logged in, then ask for log in/sign up
        '''
        response = self.client.get(reverse('ratemyrecipeapp:account'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In or Sign up here!')

    def test_my_account_view_with_authenticated_user_shows_recipes_added_and_rated(self):
        '''
        If the user has logged in, show links to the recipes ive rated and my recipes pages
        '''
        cat = create_category('British')
        usr = create_django_user()

        self.client.force_login(usr)

        response = self.client.get(reverse('ratemyrecipeapp:account'))

        self.assertEqual(response.status_code, 200)

        url = reverse('ratemyrecipeapp:my_recipes')
        self.assertContains(response, 'My Recipes')
        self.assertContains(response, url)

        url = reverse('ratemyrecipeapp:recipes_ive_rated')
        self.assertContains(response, 'My Ratings')
        self.assertContains(response, url)

# test recipes ive rated and my recipes too!
