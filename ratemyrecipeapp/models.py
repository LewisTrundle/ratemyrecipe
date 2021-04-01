from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # I think we're not adding any other attributes like web or picture?

    def __str__(self):
        return self.user.username


class Category(models.Model):
    NAME_MAX_LENGTH = 30
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    TITLE_MAX_LENGTH = 100
    TEXT_MAX_LENGTH = 1000

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    picture = models.ImageField(upload_to='recipe_images', blank=True)

    ingredients = models.TextField(max_length=TEXT_MAX_LENGTH)
    directions = models.TextField(max_length=TEXT_MAX_LENGTH)
    is_vegan = models.BooleanField()
    cost = models.PositiveSmallIntegerField()
    time_needed = models.DurationField(help_text='HH:MM:SS format')

    added_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'recipes'

    def __str__(self):
        return f'{self.title} by {self.added_by} in {self.category}'


class Rating(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rating for [{self.recipe}] by {self.rated_by}: {self.rating}'
