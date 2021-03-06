from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
from ratemyrecipeapp.models import Category, Recipe, Rating, UserProfile
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from ratemyrecipeapp.forms import RecipeForm, UserForm, UserProfileForm
from ratemyrecipe.settings import MEDIA_DIR
import os
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register



def index(request):
    context_dict = {}
    
    # Picks a random recipe
    ran_recipe = Recipe.objects.order_by('?').first()
    # Gets all the ratings associated with that recipe
    ratings = Rating.objects.filter(recipe=ran_recipe)

    # Calculates the avergae rating and stores as a dictionary
    avg_rating_dict = ratings.aggregate(Avg('rating'))
    # Gets the value in the dict
    avg_rating = avg_rating_dict['rating__avg']
    
    if avg_rating is None:
        context_dict['rating'] = 1
    else:
        context_dict['rating'] = int(avg_rating)


    context_dict['Recipe'] = ran_recipe
    

    return render(request, 'ratemyrecipeapp/index.html', context=context_dict)


def categories(request):
    categories = list(Category.objects.all())
    
    files = os.listdir(os.path.join(MEDIA_DIR, "category_images/"))
    
    context_dict = {}
    context_dict['categories'] = categories
    context_dict['files'] = files

    return render(request, 'ratemyrecipeapp/categories.html', context=context_dict)


def chosen_category(request, category_name_slug):
    context_dict = {}

    # Tries to find category name slug with given name
    # If it can't, the get() method raises DoesNotExist exception
    # get() methods returns one model instance or raises exception
    category = Category.objects.get(slug=category_name_slug)

    # Retreives all associated recipes
    # filter() returns list of recipes objects or empty list
    recipes = Recipe.objects.filter(category=category)
        
    averages = []
    for recipe in recipes:
        ratings = Rating.objects.filter(recipe=recipe)
        avg_rating_dict = ratings.aggregate(Avg('rating'))
        avg_rating = avg_rating_dict['rating__avg']
        
        if avg_rating is None:
            averages.append(1)
        else:
            averages.append(int(avg_rating))
        
        
    context_dict['recipes'] = recipes
    context_dict['category'] = category
    context_dict['ratings'] = averages

    # renders and returns response to client
    return render(request, 'ratemyrecipeapp/chosen_category.html', context=context_dict)



def random_recipe(request, recipe_name_slug):
    context_dict = {}
    
    try:
        recipe = Recipe.objects.get(slug=recipe_name_slug)
        context_dict['recipe'] = recipe
        ratings = Rating.objects.filter(recipe=recipe)
        
        # Calculates the avergae rating and stores as a dictionary
        avg_rating_dict = ratings.aggregate(Avg('rating'))
        # Gets the value in the dict
        avg_rating = avg_rating_dict['rating__avg']
        
        
        if avg_rating is None:
            context_dict['rating'] = 1
        else:
            context_dict['rating'] = int(avg_rating)
        
    except:
        context_dict['recipe'] = None
    
    return render(request, 'ratemyrecipeapp/chosen_recipe.html', context=context_dict)


@csrf_exempt
def chosen_recipe(request, category_name_slug, recipe_name_slug):
    context_dict = {}
    
    try:
        recipe = Recipe.objects.get(slug=recipe_name_slug)
        context_dict['recipe'] = recipe
        ratings = Rating.objects.filter(recipe=recipe)
        
        # Calculates the average rating and stores as a dictionary
        avg_rating_dict = ratings.aggregate(Avg('rating'))
        # Gets the value in the dict
        avg_rating = avg_rating_dict['rating__avg']
        
        
        if avg_rating is None:
            context_dict['rating'] = 1
        else:
            context_dict['rating'] = int(avg_rating)
        
        
        
    except:
        context_dict['recipe'] = None
    
    return render(request, 'ratemyrecipeapp/chosen_recipe.html', context=context_dict)



def trending(request):
    context_dict = {}
    recipe_ratings={}

    
    for recipe in list(Recipe.objects.all()):
        rating_score=0
        no_rated=0
        for rating in list(Rating.objects.filter(recipe=recipe)):
            rating_score+=rating.rating
            no_rated+=1
        try:
            recipe_ratings[recipe]=(int(rating_score/no_rated))
        except:
            #recipe not added
            pass

    #amount of recipes to show
    amount=5
    sorted_values = sorted(recipe_ratings.values(), reverse=True)# Sort the values
    print(sorted_values)
    recipes = {}

    for i in range(amount):
        for k in recipe_ratings.keys():
            if recipe_ratings[k] == max(sorted_values):
                recipes[k] = recipe_ratings[k]
                del recipe_ratings[k]
                sorted_values.remove(max(sorted_values))
                break

    context_dict['recipes']=recipes
    context_dict['amount']=amount
   

    return render(request, 'ratemyrecipeapp/trending.html', context=context_dict)
    
    
def my_account(request):
    context_dict = {}
    
    return render(request, 'ratemyrecipeapp/my_account.html', context=context_dict)


@login_required
def add_recipe(request, category_name_slug):
    # Gets the recipe form from forms.py
    form = RecipeForm()

    if request.method == 'POST':
        form = RecipeForm(request.POST,request.FILES)
        u=request.user
        user=UserProfile.objects.get(user_id=u.id)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.added_by=user
            recipe.category = Category.objects.get(slug=category_name_slug)
            recipe.save()
            return redirect(reverse('ratemyrecipeapp:index'))

        else:
            print(form.errors)
    
    context_dict = {} 
    context_dict['form']=form
    context_dict['category']=Category.objects.get(slug=category_name_slug)

    return render(request, 'ratemyrecipeapp/add_recipe.html', context=context_dict)


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
                  'ratemyrecipeapp/sign_up.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
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
            print("Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # The request is not HTTP POST, so display login form
    # This would be HTTP GET
    else:
        # No context variables to pass to template system so blank dict. object
        return render(request, 'ratemyrecipeapp/login.html')


@login_required
def user_logout(request):
    # Since we know user is logged in, we can just log them out
    logout(request)
    # Returns user to homepage
    return redirect(reverse('ratemyrecipeapp:index'))



@csrf_exempt
def rate_recipe(request):
    if request.method == 'GET':
        val = request.GET['val']
        u = request.user
        title = request.GET['title']
        
        # Gets the UserProfile associated with User
        user = UserProfile.objects.get(user=u)
        recipes = Recipe.objects.get(title=title)
            
        r = Rating.objects.create(
                rating=int(val),
                rated_by=user,
                recipe=recipes)

        r.save()
        
        return JsonResponse({'success':'true', 'rating':val}, safe=False)
    return JsonResponse({'success':'false'})



@login_required
def my_recipes(request):
    u = request.user
    user = UserProfile.objects.get(user=u)
    
    recipes = Recipe.objects.filter(added_by = user)
    
    context_dict = {}
    context_dict['recipes'] = recipes
    
    return render(request, 'ratemyrecipeapp/my_recipes.html', context=context_dict)


@login_required
def recipes_ive_rated(request):
    # Gets the user profile
    u = request.user
    user = UserProfile.objects.get(user=u)
    
    # Gets all the ratings associated with the user
    ratings = Rating.objects.filter(rated_by = user)
    
    # Gets all the recipes rated by the user
    recipes = []
    for rating in ratings:
        r = Recipe.objects.get(title = rating.recipe.title)
        recipes.append(r)
    
    
    context_dict = {}
    context_dict['recipes'] = recipes
    context_dict['ratings'] = ratings
    
    return render(request, 'ratemyrecipeapp/recipes_ive_rated.html', context=context_dict)
