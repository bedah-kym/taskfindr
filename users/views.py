from django.utils import timezone
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import registration_form, updateuser,updateprofile,activationform
from .models import Cashaccount,profile,Withdrawrequest,Leveluprequest
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import UpdateView,DeleteView
from.validators import Reffcodevalidator

def register_view(request,**kwargs):

    if request.method == "POST":
        form = registration_form (request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            phonenumber = form.cleaned_data.get('phone')
            code= kwargs['code']
            if Reffcodevalidator(code) == True:
                form.save()
                reff_code = code
                owner = User.objects.get(username=username)
                prof=profile.objects.create(user = owner,reffered_by = reff_code,phone_number=phonenumber)
                prof.save()
                messages.success(request,f'WELCOME {username} you are now a member.ACTIVATE your account now')
                return redirect('about')
            else:
                messages.warning(request,f'Sorry {username} you need a valid refferal link to register,click register to use our default link')
                return redirect(reverse("register",kwargs={"code":code}))
        else:
            pass
    else:
        form = registration_form()
    return render(request,'blog/register.html',{'form':form})

@login_required
def profile_view(request):
    account = Cashaccount.objects.get(owner=request.user)
    myprofile = profile.objects.get(user=request.user)
    if request.method == "POST":
        u_form = updateuser(request.POST, instance=request.user)
        p_form = updateprofile(request.POST, request.FILES, instance= request.user.profile)
        print(request.POST)

        if u_form.is_valid():
            u_form.save()
            messages.success(request,f'your profile has been updated ')
            return redirect('profile')
    
        
        if p_form.is_valid():
            p_form.save()
            messages.success(request,f'your profile has been updated ')
            return redirect('profile')
       
        
    u_form = updateuser(instance=request.user)
    p_form = updateprofile(instance= request.user.profile)

    context ={
    'u_form':u_form,
    'p_form':p_form,
    'errors':p_form.errors,
    'my_account':account,
    'reffs':account.refferals.all(),
    'total_reffs':account.refferals.count(),
    'my_profile':myprofile
    }

    return render(request,'blog/profile.html',context)

@login_required
def withdrawalrequest(request):
    my_user = request.user
    account= Cashaccount.objects.get(owner=my_user)
    amount = account.get_total_cash(my_user)
    if amount >= 100: # change to 1000 also change in template
        WR = Withdrawrequest.objects.create(account=account)
        WR.save()
        messages.success(request,"request sent,you will recieve an email once the agents verify your account balance")
    else:
        messages.warning(request,"sorry, you dont have enough cash GO back and continue earning")
        return redirect('home')
    return redirect ('profile')

@login_required
def levelup(request):
    my_user = request.user
    my_profile = profile.objects.get(user=my_user)
    form = activationform()
    if request.method == "POST":
        form = activationform(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('mpesa_code')
            Leveluprequest.objects.create(user_profile = my_profile,mpesa_code = code,request_date = timezone.now() )
            messages.success(request,f"Thank you {my_user} , we will verify your request and getback to you")
            return redirect('profile')
        else:
            messages.warning(request,"sorry your request is invalid check your mpesa code")  
            return redirect('profile')
    messages.info(request,f"HI {my_user} ,pay here same way as before to levelup")
    return render(request,'blog/activation.html',{"form":form})


class Cashaccountupdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model=Cashaccount
    template_name= 'blog/activation.html'
    fields=['mpesa_code']
    success_url = '/profile/'

    def test_func(self):
        Cashaccount=self.get_object()
        if self.request.user == Cashaccount.owner:
            return True
        return False


class Cashaccountdelete(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model=Cashaccount
    template_name= 'blog/account_deletion.html'
    success_url='/profile/'
    def test_func(self):
        Cashaccount=self.get_object()
        if self.request.user == Cashaccount.owner:
            return True
        return False