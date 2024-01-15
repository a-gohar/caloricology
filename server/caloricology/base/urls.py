from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("createfood", views.create_food, name="food_creator"),
    path("addfood", views.addfood, name="add_food"),
    path("weight", views.addWeight, name="Add_weight"),
    path("foodlog", views.foodlog, name="Food_log"),
    path("editday", views.edit_day, name="edit_day"),
    path('update-food-log', views.update_food_log, name='update_food_log'),
    path("foodform", views.foodForm, name="serve_food_form"),
    path("get-weights", views.get_weights, name="weight get"),
    path("settings", views.settings, name="Settings" ),
    path("get-goals", views.get_goals, name="Goals"),
    path("logout", views.logout_view, name="Logout")
]