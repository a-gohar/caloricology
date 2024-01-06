from django.db import models
import datetime

from django.utils import timezone

class food(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=1)
    cal = models.IntegerField("Calories", default=0)
    protein = models.IntegerField(default=0)
    carbs = models.IntegerField(default = 0)
    fat_g = models.IntegerField(default=0)
    def __str__(self):
        return str(self.cal) + "calories"

class macro_day(models.Model):
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE, default=1)
    date = models.DateField(default=timezone.today().date())
    calories = models.IntegerField(default = 0)
    pro = models.IntegerField(default = 0)
    fat = models.IntegerField(default = 0)
    

class savedFood(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=1)
    food_name = models.TextField("Name", default="")
    cal_100g = models.IntegerField("Calories Per 100g", default=0)
    protein_100g = models.IntegerField("Protein per 100g", default=0)
    carb_100g = models.IntegerField("Carbohydrates per 100g", default=0)
    fat_100g = models.IntegerField("Fat per 100g", default = 0)
    def __str(self):
        return str(self.cal_100g) + "cal/100g"

class weight(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=1)
    entry = models.PositiveSmallIntegerField(default='0')
    entry_date = models.DateField("Date Entered")
    def last3Weeks(self) -> bool:
        """_summary_

        Returns:
            bool: True if this weight was added in the last 3 weeks
        """
        return self.entry_date >= timezone.now().date() - datetime.timedelta(days=21)
    
