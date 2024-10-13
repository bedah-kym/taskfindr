from django.utils import timezone
from django.shortcuts import render,redirect
from django.urls import reverse
from verify_email.email_handler import send_verification_email
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import registration_form, updateuser,updateprofile,activationform
from .models import Cashaccount,profile,Withdrawrequest,Leveluprequest
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import UpdateView,DeleteView
from.validators import Reffcodevalidator
from .emails import warning_email

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
                messages.warning(request,"make sure you check your EMAIL for a verification link to LOG IN , if you dont find it check your SPAM folder")
                messages.success(request,f'WELCOME {username} you are now a member. PLEASE READ THE SITE GUIDE')
                send_verification_email(request, form)
                return redirect('about')
            else:
                messages.warning(request,f'Sorry {username} you need a valid refferal link to register,click register to use our default link')
                return redirect(reverse("register",kwargs={"code":code}))
        else:
            messages.info(request,f"sorry !! {form.errors}")
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
    existing =  Withdrawrequest.objects.filter(account=account)
    if not existing :
        amount = account.get_total_cash(my_user)
        if amount >= 1000 and account.is_valid==True: # change to 1000 also change in template
        
            WR = Withdrawrequest.objects.create(account=account)
            WR.save()
            messages.success(request,"request sent,you will recieve an email once the agents verify your account balance")
        else:
            messages.warning(request,"sorry, you dont have enough cash GO back and continue earning,also check if ur account is activated")
            return redirect('home')
    messages.info(request,"your previous withdraw request is pending verification, please wait or reach out to us via email or social media")
    return redirect ('profile')

@login_required
def levelup(request):
    my_user = request.user
    my_profile = profile.objects.get(user=my_user)
    lastlevelup = Leveluprequest.objects.filter(user_profile=my_profile)
    form = activationform()
    if not lastlevelup:
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
    messages.info(request,f"HI {my_user} ,wait while we clear your pending levelup request")
    return render(request,'blog/activation.html',{"form":form})


@login_required
def admincheckaccounts(request):
        """function that checks your last login, if ur incative for more than a month
        we send you an email then flag you as in active untill you log back in, if you dont log in we wait for two
        months then lock ur cash account.IT only works if ur admin
        """
        if request.user.is_staff or request.user.is_superuser:
            allusers = User.objects.all()
            accounts_warned=0
            accounts_reposessed=0
            accounts_checked=0 
            for myuser in allusers:
                if myuser.last_login and myuser.is_superuser==False:
                    last_login = myuser.last_login.month
                    last_login_day = myuser.last_login.day
                    this_month = timezone.now().month
                    today = timezone.now().day
                    if last_login < this_month:
                        #if you last logged in last month check below which day of last month did you log  in and comapre with todays date
                        if (this_month - last_login) == 1:
                            """logic here is that if you minus todays date ie 16 (aug)with any date from last month eg 30 (july) it will
                            always give you a negative number unless the difference between the dates is a month.ie 16aug -16july ==0 
                            which will mean a month has passed 
                            """
                            warning_email(myuser,"warn")
                            if (today-last_login_day) >= 0:
                                accounts_warned+=1
                                accounts_checked+=1 
                            accounts_checked+=1
                        elif (this_month - last_login) >=3:
                            warning_email(myuser," ")
                            accounts_reposessed+=1
                            accounts_checked+=1 
                            Cashaccount.reposess_account(myuser)
                            if myuser.is_active:
                                myuser.is_active=False
                                myuser.save()
                    accounts_checked+=1
                    ctx={
                    "checked":accounts_checked,
                    "reposessed":accounts_reposessed,
                    "warned":accounts_warned,
                    "totalusers":allusers.count()
                    }
        else:
            messages.warning(request,"your not an authorised mf! ")
            return redirect('home')
        
        return render(request,'blog/accountchecker.html',ctx)

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