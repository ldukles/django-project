from django.contrib import admin
from .models import Observation, Category, Photo, Location

# Register your models here
admin.site.register(Observation)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Location)
