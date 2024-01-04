from django.db import models


class food(models.Model):
    cal = models.IntegerField("Calories", default=0)
    protein = models.IntegerField(default=0)
    
