from django.contrib import admin
from .models import blogpost

class blogpostadmin(admin.ModelAdmin):
    list_display = ('author','date_posted','spaces')
    list_filter=['date_posted']

admin.site.register(blogpost,blogpostadmin)
