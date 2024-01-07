from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.template import loader
from .models import food, savedFood, weight
from django.contrib.auth.decorators import login_required
from .forms import saveFoodForm

def index(request):
    return HttpResponse("<h1> WIP <h1>")

@login_required
def dashboard(request):
    pass

@login_required
def addfood(request):
    pass

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
        return HttpResponseRedirect("/dashboard/")
