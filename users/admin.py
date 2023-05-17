from django.contrib import admin
from .models import profile,Cashaccount,Withdrawrequest

class profileadmin(admin.ModelAdmin):
    list_display = ('user','phone_number','reffered_by')
    search_fields = ('user__username',)

    
class cashaccountadmin(admin.ModelAdmin):
    list_display = ('owner','mpesa_code','is_valid')
    list_filter = ['is_valid']
    search_fields=['owner__username']

class withdrawrequestadmin(admin.ModelAdmin):
    search_fields=['request_date']

admin.site.register(profile,profileadmin)
admin.site.register(Cashaccount,cashaccountadmin)
admin.site.register(Withdrawrequest, withdrawrequestadmin)