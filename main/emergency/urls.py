from .views import *
from django.urls import path

urlpatterns = [

    path('login', login_json, name="login_json"),
    path('help', Emergency_response, name="help"),
    path('cities', get_cities, name="cities"),
    path('categories', get_categories, name="categories"),
    path('helplist', get_Emergencies, name="helplist"),
    path('helps/<str:id>', get_Emergency, name="helps"),
    path('blog', get_blogpost, name='blog'),
    path('blog/<str:id>', get_blogpost_page, name='blog_page'),
    path('addblog', add_blogpost, name='add_blogpost')
]