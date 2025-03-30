from .views import *
from django.urls import path

urlpatterns = [

    path('help', Emergency_response, name="help"),

]