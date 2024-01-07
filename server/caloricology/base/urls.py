from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("createfood", views.create_food, name="food_creator"),
    path("addfood", views.addfood, name="add_food")
]