from .views import *
from django.urls import path

urlpatterns = [

    path('help', Emergency_response, name="help"),
    path('cities', get_cities, name="cities"),
    path('helplist', get_Emergencies, name="helplist"),
    path('helps', get_Emergency, name="helps"),
]