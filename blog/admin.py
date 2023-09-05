from django.contrib import admin
from django.db import models
from .models import blogpost,Postreaction,WheelSpin

class blogpostadmin(admin.ModelAdmin):
    list_display = ('author','date_posted','spaces')
    list_filter=['date_posted']

admin.site.register(blogpost,blogpostadmin)
admin.site.register(Postreaction)
admin.site.register(WheelSpin)