import requests
from .models import macro_day, food
from .keys import KEY

def usda_api(query):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    url += "?api_key=" + KEY

    payload = {
        "query": query,
        'dataType': ["Survey (FNDDS)", "Branded"]
    }

    # Headers
    headers = {
        "Content-Type": "application/json"
    }

    res = []

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        res = []
        for item in data["foods"][0:4]:
            nutrients = item["foodNutrients"]
            res.append({"name": item["description"], "protein":  nutrients[0]["value"],
                       "fat":  nutrients[1]["value"], "carb":  nutrients[2]["value"],
                       "calories": nutrients[3]["value"]})
        return res
    else:
        return False

def update_macro_day(dayObject, jsonData):
    try:
        totalCalories = (float(jsonData["calories"]) * int(jsonData["weight"])) // 100
        totalProtein = (float(jsonData["protein"]) * int(jsonData["weight"])) // 100
        totalCarb = (float(jsonData["carb"]) * int(jsonData["weight"])) // 100
        totalFat = (float(jsonData["fat"]) * int(jsonData["weight"])) // 100
        foodObject = food.objects.create(day = dayObject, cal = totalCalories, 
                                        protein = totalProtein, carbs = totalCarb, fat=totalFat,
                                        name=jsonData["food_name"])
        dayObject.calories += totalCalories
        dayObject.pro += totalProtein
        dayObject.carbs += totalCarb
        dayObject.fat += totalFat
        dayObject.save()
        return True
    except Exception as e:
        print(e)
        return False
    