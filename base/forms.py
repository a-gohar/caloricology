from django import forms
from .models import user_goals, savedFood
from datetime import datetime

class weightForm(forms.Form):
    date = forms.DateField(label="Date", widget=forms.SelectDateWidget, initial=datetime.now())
    weight = forms.IntegerField(label="Weight", min_value=0, max_value=500)
class editDayForm(forms.Form):
    date = forms.DateField(label="Date you wish to edit:")
    new_cal = forms.IntegerField(label="New calories:", min_value=0, max_value=20000)

class userGoalsForm(forms.ModelForm):
    class Meta:
        model = user_goals
        fields = ['weekly_target', 'tdee']
  
class addFoodForm(forms.Form):
    date = forms.DateField(label="What day do you want to add food?", widget=forms.SelectDateWidget, initial=datetime.now())
    food_name = forms.ModelChoiceField(queryset=savedFood.objects.all(), empty_label="Select a food")
    volume = forms.IntegerField(label="Weight in grams?")
class saveFoodForm(forms.Form):
    food_name = forms.CharField(label="Food name", min_length=1, max_length=100)
    cal_100 = forms.IntegerField(label="Calories per 100g", min_value=0, max_value=900)
    fat_100 = forms.IntegerField(label="Fat per 100g", min_value=0, max_value=100)
    protein_100 = forms.IntegerField(label="Protein per 100g", min_value=0, max_value=100)
    carb_100 = forms.IntegerField(label="Carbohydrate per 100g", min_value=0, max_value=100)

class commonFoodForm(forms.Form):
    food_query = forms.CharField(label="Food to search?", min_length=3, max_length=100)