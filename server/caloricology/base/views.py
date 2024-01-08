from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.template import loader
from .models import food, savedFood, weight, macro_day
from django.contrib.auth.decorators import login_required
from .forms import saveFoodForm, editDayForm, addFoodForm, weightForm


def index(request):
    return HttpResponse("<h1> WIP <h1>")

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
            weight.objects.create(entry_date=day[0], entry=data["weight"])
            return HttpResponseRedirect("dashboard")
        except Exception as e:
            print(e)
            return HttpResponseBadRequest()


@login_required
def edit_day(request):
    if request.method == "GET":
        form = editDayForm()
        return render(request, "base/editday.html", {"form": form} )
    else:
        pass
        
@login_required
def addfood(request):
    if request.method == "GET":
        form = addFoodForm()
        return render(request, "base/addfood.html", {"form": form})
    if request.method == "POST":
        try:
            form = addFoodForm(request.POST)
            if not form.is_valid():
                print("FAIL")
                return HttpResponseBadRequest("Invalid form")
            data = form.cleaned_data
            today = macro_day.objects.get_or_create(owner=request.user, date=data["date"])
            foodPerc = savedFood.objects.get(owner=request.user, food_name=data["food_name"])
            calories = foodPerc.cal_100g * data["volume"] // 100
            protein = foodPerc.protein_100g * data["volume"] // 100
            fat = foodPerc.fat_100g * data["volume"] // 100
            carb = foodPerc.carb_100g * data["volume"] // 100
            food.objects.create(day=today[0] , name=data["food_name"], 
                                cal=calories, protein=protein, fat=fat, carbs=carb)
            return HttpResponseRedirect("/dashboard")
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
        return HttpResponseRedirect("/dashboard")
