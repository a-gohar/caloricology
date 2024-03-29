from django.db import models
import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class user_goals(models.Model):
    owner = models.OneToOneField("accounts.User", on_delete=models.CASCADE, default=1)
    goal_choices = [
        ('maintain', 'Maintain'),
        ('gain', 'Gain Weight'),
        ('lose', 'Lose Weight'),
    ]
    experience_choices = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    goal = models.CharField(max_length=10, choices=goal_choices, default='maintain')
    experience = models.CharField(max_length=25, choices=experience_choices, default='beginner')
    tdee = models.IntegerField(default=1000)
    pRatio = models.IntegerField(default=50)
    weekly_target = models.FloatField(default=0, validators=[
            MaxValueValidator(100),
            MinValueValidator(-100)
        ])
    
class macro_day(models.Model):
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE, default=1)
    date = models.DateField(default="2024-01-01")
    weight = models.FloatField(default = 0)
    calories = models.IntegerField(default = 0)
    pro = models.IntegerField(default = 0)
    fat = models.IntegerField(default = 0)
    carbs = models.IntegerField(default=0)
    def newWeight(self, new_weight):
        self.weight = new_weight
    def __str__(self):
        return str(self.date) + ": " + str(self.calories) + str(self.weight)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['owner', 'date'], name="Unique_tuple")]
    
class food(models.Model):
    day = models.ForeignKey("macro_day", on_delete=models.CASCADE, default=1)
    name = models.CharField("Name", default="", max_length=302)
    cal = models.IntegerField("Calories", default=0)
    protein = models.IntegerField(default=0)
    carbs = models.IntegerField(default = 0)
    fat = models.IntegerField(default=0)
    def __str__(self):
        return str(self.cal) + "calories"

class savedFood(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=1)
    food_name = models.CharField(default="", max_length=300)
    cal_100g = models.IntegerField("Calories Per 100g", default=0)
    protein_100g = models.IntegerField("Protein per 100g", default=0)
    carb_100g = models.IntegerField("Carbohydrates per 100g", default=0)
    fat_100g = models.IntegerField("Fat per 100g", default = 0)
    def __str__(self):
        return self.food_name
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'food_name'], name='unique_food_tuple')
        ]

