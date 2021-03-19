from django.shortcuts import render
from django.http import HttpResponse
from ratemyrecipeapp.models import Category, Recipe, Rating
<<<<<<< HEAD
import random
=======
#from Random import random
>>>>>>> 4e04a2e9debe17ddc3ed54f93e4bba308beb1560
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from ratemyrecipeapp.forms import RecipeForm


def index(request):

    # Gets a list of every recipe
    recipes = list(Recipe.objects.all())
    # Picks a random recipe
<<<<<<< HEAD
    ran_recipe = random.sample(recipes, 1)

    rating = Rating.objects.filter(recipe=ran_recipe)

    context_dict = {}
    context_dict['welcome'] = "Welcome to Rate My Recipe!"
    context_dict['ran_recipe'] = ran_recipe
    context_dict['rating'] = rating
=======
    #ran_recipe = random.sample(recipes, 1)
    
    #rating = Rating.objects.filter(recipe=ran_recipe)
    
    
    
    context_dict = {}
    context_dict['welcome'] = "Welcome to Rate My Recipe!"
    #context_dict['ran_recipe'] = ran_recipe
    #context_dict['rating'] = rating
    
    return render(request, 'index.html', context=context_dict)

>>>>>>> 4e04a2e9debe17ddc3ed54f93e4bba308beb1560

    return render(request, 'ratemyrecipeapp/index.html', context=context_dict)


def categories(request):
    categories = list(Category.objects.all())

    context_dict = {}
    return render(request, 'categories.html', context=context_dict)


def chosen_category(request, category_name_slug):
    context_dict = {}

    try:
        # Tries to find category name slug with given name
        # If it can't, the get() method raises DoesNotExist exception
        # get() methods returns one model instance or raises exception
        category = Category.objects.get(slug=category_name_slug)

        # Retreives all associated recipes
        # filter() returns list of recipes objects or empty list
        recipes = Recipe.objects.filter(category=category)

        # Adds results list to template context under name recipes
        context_dict['recipes'] = recipes
        # Adds category object from database to dict - used to verify category exists
        context_dict['category'] = category

    except:
        # If specified category can't be found, template will display "no category" message
        context_dict['category'] = None
        context_dict['recipes'] = None

    # renders and returns response to client
    return render(request, 'ratemyrecipeapp/chosen_category.html', context=context_dict)


def trending(request):
    pass


<<<<<<< HEAD
=======

def add_recipe(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
      
    # if attempting to add page to category that doesn't exist
    if category is None:
        return redirect('/ratemyrecipe/')
    
    
    # Gets the recipe form from forms.py
    form = RecipeForm()
    
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        
        if form.is_valid():
            if category:
                recipe = form.save(commit=False)
                recipe.category = category
                recipe.save()
                
                return redirect('categories', kwargs={'category_name_slug': category_name_slug})
            
        else:
            print(form.errors)
            
    context_dict = {'form': form, 'category': category}
    return render(request, 'add_recipe.html', context=context_dict)
    
        



>>>>>>> 4e04a2e9debe17ddc3ed54f93e4bba308beb1560
def sign_up(request):
    # Is registration successful?
    registered = False

    if request.method == 'POST':
        # Attempt to grab info from raw form information
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save user's form data to database
            user = user_form.save()

            # Set then update password
            user.set_password(user.password)
            user.save()

            # Set commit=False to delay saving model
            # until ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # If profile pic provided, get it from input form
            # and put it in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Saves UserProfile instance
            profile.save()

            # Update variable to indicate to template registration was successful
            registered = True
        else:
            # Invalid form(s)
            # Prints problems to terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not an HTTP POST so form rendered using two ModelForm instances
        # These forms will be blank, ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render template depending on context
    return render(request,
                  'ratemyrecipeapp/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def login(request):
    # If request is HTTP POST, try to pull relevant info
    if request.method == 'POST':
        # Get username and password from login form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # If username/password combination valid, User object is returned
        user = authenticate(username=username, password=password)

        # If we have as User object, the details are correct
        # If None, no user with matching credential found
        if user:
            # Is account active?
            if user.is_active:
                # If account valid and active, log user in and send back to homepage
                login(request, user)
                return redirect(reverse('ratemyrecipeapp:index'))
            else:
                # An inactive account was used so doesn't log in
                return HttpResponse("Your RateMyRecipe account is disabled.")
        else:
            # Bad login details provided, so doesn't log in
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # The request is not HTTP POST, so display login form
    # This would be HTTP GET
    else:
        # No context variables to pass to template system so blank dict. object
<<<<<<< HEAD
        return render(request, 'ratemyrecipeapp/login.html')


=======
        return render(request, 'login.html')
    
    
>>>>>>> 4e04a2e9debe17ddc3ed54f93e4bba308beb1560
@login_required
def user_logout(request):
    # Since we know user is logged in, we can just log them out
    logout(request)
    # Returns user to homepage
    return redirect(reverse('ratemyrecipeapp:index'))


def my_account(request):
    pass


def my_recipes(request):
    pass


def recipes_ive_rated(request):
    pass
