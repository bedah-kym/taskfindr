from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404


def Phonenumbervalidator(num):
    #use regex so phone numbers are kenyan 
    pass

def Mpesacodevalidator(code):
    # regex to make shure the format is legit
    pass

def Reffcodevalidator(reff_code):
    # we dont want fake reffcodes
    try:
        get_object_or_404(User,username=reff_code)
        return True
    except Http404:
        print('invalid refferal link')#report this incident
        return False
