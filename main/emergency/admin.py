from django.contrib import admin
# Register your models here.
from .models import *


admin.site.register(City)
admin.site.register(Categories)
admin.site.register(EmergencyRequest)
admin.site.register(Suppliers)
admin.site.register(Blogpost)
admin.site.register(State)