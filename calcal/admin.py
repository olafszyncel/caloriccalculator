from django.contrib import admin
from .models import User, Profile, Dinner, Lunch, Breakfast

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Dinner)
admin.site.register(Lunch)
admin.site.register(Breakfast)
