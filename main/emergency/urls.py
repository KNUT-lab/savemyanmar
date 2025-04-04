from .views import *
from django.urls import path

urlpatterns = [

    path('login', login_json, name="login_json"),
    path('help', Emergency_response, name="help"),
    path('cities', get_cities, name="cities"),
    path('categories', get_categories, name="categories"),
    path('helplist', get_Emergencies, name="helplist"),
    path('helps/<str:id>', get_Emergency, name="helps"),
]