from django import forms


class saveFoodForm(forms.Form):
    food_name = forms.CharField(label="Food name", max_length=100)
    cal_100 = forms.IntegerField(label="Cal per 100g", min_value=0, max_value=900)
    fat_100 = forms.IntegerField(label="Fat per 100g", min_value=0, max_value=100)
    protein_100 = forms.IntegerField(label="Protein per 100g", min_value=0, max_value=100)
    carb_100 = forms.IntegerField(label="Carbohydrate per 100g", min_value=0, max_value=100)