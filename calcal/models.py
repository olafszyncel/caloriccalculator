from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    weight = models.DecimalField(max_digits=6, decimal_places=1)
    tall = models.IntegerField()
    year_birth = models.CharField(max_length=4)
    activity_lvl = models.DecimalField(max_digits=3, decimal_places=1)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    goal_weight = models.IntegerField()
    rate = models.IntegerField()
    caloric = models.IntegerField()
    
class Breakfast(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    product = models.CharField(max_length=200, default='any_name')
    product_weight = models.IntegerField(default=0)
    caloric = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    day = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.pk,
            "product": self.product,
            "gram": self.product_weight,
            "caloric": self.caloric,
            "fat": self.fat,
            "carbs": self.carbs,
            "protein": self.protein,
            "day": self.day,
        }

class Lunch(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    product = models.CharField(max_length=200, default='any_name')
    product_weight = models.IntegerField(default=0)
    caloric = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    day = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.pk,
            "product": self.product,
            "gram": self.product_weight,
            "caloric": self.caloric,
            "fat": self.fat,
            "carbs": self.carbs,
            "protein": self.protein,
            "day": self.day,
        }

class Dinner(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    product = models.CharField(max_length=200, default='any_name')
    product_weight = models.IntegerField(default=0)
    caloric = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbs = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    day = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.pk,
            "product": self.product,
            "gram": self.product_weight,
            "caloric": self.caloric,
            "fat": self.fat,
            "carbs": self.carbs,
            "protein": self.protein,
            "day": self.day,
        }


