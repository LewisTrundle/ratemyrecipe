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
    error_message = 'Please enter the time in the format HH:MM. For example, 01:30 for an hour and a half.'

    title = forms.CharField(
        max_length=Recipe.TITLE_MAX_LENGTH,
        help_text='Recipe title'
    )
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    ingredients = forms.CharField(
        max_length=Recipe.TEXT_MAX_LENGTH,
        widget=forms.Textarea(attrs={'style': "width:100%;"}),
        help_text='What ingredients do you need?'
    )
    directions = forms.CharField(
        max_length=Recipe.TEXT_MAX_LENGTH,
        widget=forms.Textarea(attrs={'style': "width:100%;"}),
        help_text='How do you cook this amazing recipe?'
    )

    is_vegan = forms.BooleanField(required=False,
                                  help_text="Vegan Recipe")
    is_vegetarian = forms.BooleanField(required=False,
                                       help_text="Vegetarian Recipe")
    cost = forms.IntegerField(
        min_value=0,
        help_text='How much does this recipe cost?',
        error_messages={'invalid': 'Please enter a positive number.'},
    )
    time_needed = forms.CharField(
        max_length=Recipe.TIME_NEEDED_MAX_LENGTH,
        help_text='How long does it take to make this? (HH:MM)',
        # idk how to change this honestly
    )

    def clean_time_needed(self):
        time_needed = self.cleaned_data['time_needed']

        if len(time_needed) != Recipe.TIME_NEEDED_MAX_LENGTH:
            self.add_error(
                'time_needed',
                RecipeForm.error_message
            )

        return time_needed

    picture = forms.ImageField(
        help_text='Insert a photo of your recipe:'
    )

    class Meta:
        model = Recipe

        exclude = ('added_by', 'slug', 'category')


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
