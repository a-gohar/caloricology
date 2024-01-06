from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from .models import food, savedFood, weight
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("<h1> WIP <h1>")

@login_required
def dashboard(request):
    foods.