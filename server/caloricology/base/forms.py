from django import forms

class weightForm(forms.Form):
    date = forms.DateField(label="Date")
    weight = forms.IntegerField(label="Weight", min_value=0, max_value=500)
class editDayForm(forms.Form):
    date = forms.DateField(label="Date you wish to edit:")
    new_cal = forms.IntegerField(label="New calories:", min_value=0, max_value=20000)


class addFoodForm(forms.Form):
    date = forms.DateField(label="What day do you want to add food?")
    food_name = forms.CharField(label="Food name?", max_length=300)
    volume = forms.IntegerField(label="Weight in grams?")
class saveFoodForm(forms.Form):
    food_name = forms.CharField(label="Food name", max_length=100)
    cal_100 = forms.IntegerField(label="Cal per 100g", min_value=0, max_value=900)
    fat_100 = forms.IntegerField(label="Fat per 100g", min_value=0, max_value=100)
    protein_100 = forms.IntegerField(label="Protein per 100g", min_value=0, max_value=100)
    carb_100 = forms.IntegerField(label="Carbohydrate per 100g", min_value=0, max_value=100)