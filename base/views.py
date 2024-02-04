from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.template import loader
from .models import food, savedFood, macro_day, user_goals
from django.contrib.auth.decorators import login_required
from .forms import saveFoodForm, editDayForm, addFoodForm, weightForm, userGoalsForm, commonFoodForm
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views import generic
from datetime import date, timedelta
from .helpers import update_macro_day, usda_api
import json
import requests

# The weight class was moved to one to one
def index(request):
    return render(request, "base/index.html")

@login_required
def foodlog(request):
    if request.method == "GET":
        return render(request, "base/foodlog.html", {"Username": request.user.first_name})
    
@login_required
def get_goals(request):
    goalObject = user_goals.objects.get_or_create(owner=request.user)[0]
    i = 21
    serialized_days = []
    while i >= 0:
        day = date.today() - timedelta(i)
        i -= 1
        entry = macro_day.objects.get_or_create(owner=request.user, date=day)[0]
        serialized_days.append({"cal": entry.calories, "weight": entry.weight})
    serialized_data= {"tdee": goalObject.tdee, "pRatio": goalObject.pRatio, "target": goalObject.weekly_target}
    return JsonResponse({"goals": serialized_data, "days" : serialized_days})
    
@login_required
def get_weights(request):
    day = macro_day.objects.filter(owner=request.user)
    serialized_data = []
    for entry in day:
        if entry.weight > 0:
            serialized_data.append({"Date": str(entry.date), "weight": entry.weight})
    return JsonResponse({"weights":serialized_data})
    
@login_required
def update_goals(request):
    if request.method == "POST":
        pass

@login_required
def update_food_log(request):
    date = request.GET.get('date')
    macro = macro_day.objects.get_or_create(date=date[0:10], owner=request.user)
    # Assuming FoodEntry model has a field 'date' representing the date of the entry
    food_entries = food.objects.filter(day=macro[0])
    # You may need to serialize the data appropriately based on your model structure
    serialized_data = [{'name': entry.name, 'calories': entry.cal, 'protein': entry.protein,
                        'fat': entry.fat, 'carbs': entry.carbs} for entry in food_entries]
    # Return the serialized data as JSON
    return JsonResponse({'food_log': serialized_data})
    
@login_required
def dashboard(request):
    if request.method == "GET":
        try:
            days = macro_day.objects.filter()
            return render(request, "dashboard.html", {"Username": request.user.first_name})
        except Exception as e:
            print(e)
            return HttpResponse()


@login_required
def addWeight(request):
    if request.method == "GET":
        form = weightForm()
        return render(request, "base/weight.html", {"form": form})
    if request.method == "POST":
        try:
            form = weightForm(request.POST)
            if not form.is_valid():
                return HttpResponseBadRequest("Error with your form")
            data = form.cleaned_data
            day = macro_day.objects.get_or_create(owner=request.user, date=data["date"])
            day[0].weight = data["weight"]
            day[0].save()
            return HttpResponse(status=204)
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Bad request")


@login_required
def edit_day(request):
    if request.method == "GET":
        form = editDayForm()
        return render(request, "base/editday.html", {"form": form} )
    else:
        pass

def foodForm(request):
    form = addFoodForm()
    return render("base/addfood.html", {"form": form}, request=request)
        
@login_required
def addfood(request):
    if request.method == "GET":
        form = addFoodForm()
        form.fields['food_name'].queryset = savedFood.objects.filter(owner=request.user)
        return HttpResponse(loader.render_to_string("base/addfood.html", 
                                                    {"form": form}, request))
    if request.method == "POST":
        try:
            form = addFoodForm(request.POST)
            if not form.is_valid():
                return HttpResponseBadRequest("Invalid form")
            data = form.cleaned_data
            today = macro_day.objects.get_or_create(owner=request.user, date=data["date"])
            today = today[0]
            foodPerc = savedFood.objects.get(owner=request.user, food_name=data["food_name"])
            calories = foodPerc.cal_100g * data["volume"] // 100
            today.calories += calories
            protein = foodPerc.protein_100g * data["volume"] // 100
            today.pro += protein
            fat = foodPerc.fat_100g * data["volume"] // 100
            carb = foodPerc.carb_100g * data["volume"] // 100
            today.fat += fat
            today.carbs += carb
            today.save()
            food.objects.create(day=today , name=data["food_name"], 
                                cal=calories, protein=protein, fat=fat, carbs=carb)
            return HttpResponse(status=204)
        except Exception as e :
            print(e)
            return HttpResponseBadRequest("Error", status=405)
        

@login_required
def create_food(request):
    if request.method == "GET":
        form = saveFoodForm()
        return render(request, "base/createfood.html", {"form": form})
    else:
        form = saveFoodForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Invalid form")
        data = form.cleaned_data
        food = savedFood.objects.create(owner=request.user, food_name=data["food_name"], 
                                        cal_100g = data["cal_100"], protein_100g= data["protein_100"],
                                        fat_100g=data["fat_100"], carb_100g=data["carb_100"])
        return HttpResponse(status=204)

@login_required
def settings(request):
    user = request.user
    user_goals_obj = user_goals.objects.get_or_create(owner=user)[0]
    if request.method == 'POST':
        form = userGoalsForm(request.POST, instance=user_goals_obj)
        if form.is_valid():
            form.save()
        if user_goals_obj.weekly_target > 0:
            user_goals_obj.pRatio = 50
        else:
            user_goals_obj.pRatio = 15
        user_goals_obj.save()
        return HttpResponse(status=204)
    else:
        form = userGoalsForm(instance=user_goals_obj)

    return render(request, 'base/settings.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("index")

@login_required
def delete_food(request):
    if request.method == "GET":
        return HttpResponseBadRequest(status=400)
    else:
        try:
            data = json.loads(request.body)
            food_name = data['food_name']
            food_date = data['food_date'][0:10]
            calories = data['calories']
            macro_object = macro_day.objects.get_or_create(owner=request.user, date=food_date )[0]
            food.objects.filter(day=macro_object, name=food_name, cal=calories)[0].delete()
            return JsonResponse({'status': 'success'})
        except Exception as e :
            return HttpResponseBadRequest("Error", status=400)
        
@login_required
def download_data(request):
    macro_day_objects = macro_day.objects.filter(owner=request.user)
    serialized_data = [{"date":entry.date, "weight": entry.weight, "calories": entry.calories} for entry in macro_day_objects ]
    return JsonResponse({"data": serialized_data})

@login_required
def common_food_search(request):
    if request.method == "POST":
        try:
            form = commonFoodForm(request.POST)
            if not form.is_valid():
                return JsonResponse({"error": {"code": "403"}})
            data = form.cleaned_data
            query = data["food_query"]
            foodResults = usda_api(query)
            return JsonResponse({"foods": foodResults})
        except Exception as e:
            print(e)
            return JsonResponse({"error": {"code": "400"}})
    else:
        return render(request, "base/commonfood.html", {"form": commonFoodForm()})

@login_required
def common_food_log(request):
    if request.method ==  "POST":
        try: 
            data = json.loads(request.body)
            print(data)
            macroDayObject = macro_day.objects.get_or_create(date=data["date"], owner=request.user)[0]
            print(macroDayObject)
            response = update_macro_day(macroDayObject, data)
            if response:
                return JsonResponse({"success": {"id": "common_food"}})
            else:
                print("error")
                return JsonResponse({"error": {"code": "400" }})
        except Exception as e:
            print(e)
            return JsonResponse({"error": {"code": "400"}})