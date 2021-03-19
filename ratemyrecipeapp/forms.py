from django import forms
from ratemyrecipe.app.models import Recipe, Category, UserProfile, Rating,

class RecipeForm(forms.ModelForm):
    title = models.CharField(max_length=100,
                             help_text="Please enter the name of the recipe.")
    #category
    ingredients = models.TextField()
    directions = models.TextField()
    is_vegan = models.BooleanField()
    cost = models.PositiveSmallIntegerField()
    time_needed = models.DurationField(help_text='HH:MM:SS format')
    
    class Meta:
        model = Recipe
        fields = ('title',)
        
        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields= ('username',)
        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile