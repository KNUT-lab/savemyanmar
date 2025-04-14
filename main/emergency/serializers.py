# serializers.py
from rest_framework import serializers
from .models import *
from django.db.models import Sum


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRequest
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    cat_names = serializers.SerializerMethodField()

    class Meta:
        model = Suppliers
        fields = '__all__'
    def get_cat_names(self, c):
        category_name = [ category.name for category in c.cat.all()]
        print(category_name)
        return category_name

class BlogpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogpost
        fields = '__all__'