from django import forms
from django.contrib.auth.models import User
from ratemyrecipeapp.models import Category, Recipe, Rating
from ratemyrecipeapp.models import UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=Category.NAME_MAX_LENGTH,
        help_text='Please enter the category name.'
    )
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    picture = forms.ImageField(
        help_text='Insert a category image here.'
    )

    class Meta:
        model = Category
        fields = ('name', 'picture', )


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        max_length=Recipe.TITLE_MAX_LENGTH,
        help_text='Recipe title'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        to_field_name='name',
        empty_label='(Category)',
        help_text='Select a category.'
    )
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    ingredients = forms.CharField(
        max_length=Recipe.TEXT_MAX_LENGTH,
        widget=forms.Textarea,
        empty_value='What ingredients do you need?'
    )
    directions = forms.CharField(
        max_length=Recipe.TEXT_MAX_LENGTH,
        widget=forms.Textarea(),
        empty_value='How do you cook this amazing recipe?'
    )
    is_vegan = forms.BooleanField(required=False)
    is_vegetarian = forms.BooleanField(required=False)
    cost = forms.IntegerField(
        min_value=0,
        error_messages={'invalid': 'Please enter a positive number.'},
    )
    time_needed = forms.DurationField(
        help_text='How long does it take to make this? HH:MM:SS',
        # idk how to change this honestly
    )

    picture = forms.ImageField(
        help_text='Insert a photo of your recipe!'
    )

    class Meta:
        model = Recipe
        exclude = ('added_by', 'slug', )


class RatingForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, max_value=1,
        help_text='Rate this recipe!',
        # see other options in django-starfield
    )

    class Meta:
        model = Recipe
        exclude = ('recipe', 'rated_by', )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ()
