from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # I think we're not adding any other attributes like web or picture?

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)  # does it have to be unique?
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    ingredients = models.TextField(max_length=1000)
    directions = models.TextField(max_length=1000)
    is_vegan = models.BooleanField()
    cost = models.PositiveSmallIntegerField()
    time_needed = models.IntegerField(help_text='HH:MM:SS format')

    added_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.added_by}'


class Rating(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rating for {self.recipe} by {self.rated_by}'
