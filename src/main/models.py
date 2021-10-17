from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from djchoices import ChoiceItem, DjangoChoices

User = get_user_model()


class City(models.Model):
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="cities", default="cities/default.png")

    def __str__(self):
        return self.name


class CuisineType(models.Model):
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="cuisines", default="cuisines/default.png")

    def __str__(self):
        return self.name


class Reward(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GenderChoices(DjangoChoices):
    male = ChoiceItem("m", "Мужской")
    female = ChoiceItem("f", "Женский")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=200, default="Пользователь", blank=True)
    photo = models.ImageField(upload_to="avatars", default="avatars/default.png")
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, default=None, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET(None), null=True, blank=True, related_name="profiles")

    def __str__(self):
        return f"{self.full_name}, {self.user.email}"


class Restaurant(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    photo = models.ImageField(upload_to="restaurant/%Y/%m/%d", default="restaurant/%Y/%m/%d", blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, related_name="restaurant")
    cuisine_type = models.ForeignKey(CuisineType, on_delete=models.CASCADE, blank=False, null=True,
                                     related_name="restaurant")
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=200, blank=True)
    site = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    rewards = models.ManyToManyField(Reward, related_name="restaurant", blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    date = models.DateField(auto_now=True)


class Dish(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    weight = models.IntegerField(null=False, blank=False)
    recipe = models.TextField(max_length=256)
    price = models.IntegerField(default=None, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=False, related_name="dishes")

    def __str__(self):
        return self.name
