from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import weight, macro_day

class User(AbstractUser):
    class goalStatus(models.TextChoices):
        GAIN = "G", _("Gain")
        MAINTAIN = "M", _("Maintain")
        LOSE = "L", _("Lose")
    goal_status = models.CharField(max_length=1, choices=goalStatus.choices, default=goalStatus.MAINTAIN)
    tdee = models.SmallIntegerField(default=2000)
    mus_percentage = models.IntegerField(min=0, max=100, )
    # def update_tdee(self):
    #     weights = weight.objects.filter(owner=self.kwargs['pk'])
    #     macros = macro_day.objects.filter(owner=self.kwargs['pk'])
    #     if not weights.count() < 3 or not macros.exists() < 1:
    #         return 0
