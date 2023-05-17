from django.db.models.signals import post_save
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Cashaccount as Ca,Withdrawrequest as Wr
from django.dispatch import receiver
from .models import profile


@receiver(post_save,sender=profile)
def create_account(sender,instance,created,**kwargs):
    if created:
        Ca.objects.create(owner = instance.user)
        
@receiver(post_save,sender=Ca)
def track_refferal(sender,instance,created,**kwargs):
    """ get the profile from the owner of the cash a/c , then get the reff_code from the profile. use the ref code to get
    the user then get that users account .if both the refferer and reffered accounts are valid add the reffered to the
    refferers refferals list.
    """
    if created:
        print('no tracking refferal..')
    else:
        if instance.has_withdrawn == True or instance.withdraw_failed == True:
            pass
        else:
            print('tracking refferal.....')
            refferedprofile = profile.objects.get(user = instance.owner)
            refferercode = refferedprofile.reffered_by
            reffereruser = User.objects.get(username=refferercode)
            refferer_ac = Ca.objects.get(owner=reffereruser)
            if refferer_ac.is_valid == True and instance.is_valid ==True:
                refferer_ac.refferals.add(refferedprofile)
            else:
                print("failed refferal track.. check if both accounts are validated.")

@receiver(post_save,sender=Ca)
def send_email(sender,created,instance,**kwargs):
    """ this function sends email to the user under 3 circumstances
    1. if the account is created
    2. if you want to withdraw
    3. if your withdrawal fails
    """
    if created:
        to_email = instance.owner.email
        from_email = 'bedankimani860@gmail.com'
        print('sending greeting email to',to_email)
        send_mail(
            'WELCOME TO TASKfindr',
            f'Hi,{instance.owner.username} thank you for joining our site we made this site so people like you can earn so giddy up and activate your account to start earning.',
            from_email,
            [to_email],
            fail_silently=False,
        )
        
    else:
        if instance.is_valid:
            
            to_email = instance.owner.email
            from_email = 'bedankimani860@gmail.com'
            if instance.has_withdrawn:
                print('sending withdraw success email to',to_email)
                try:
                    send_mail(
                'TASKfindr withdrawal success',
                f'Hi,{instance.owner.username} your withdrawal request is successfull, we will send you the amount on your phone number shortly.',
                from_email,
                [to_email],
                fail_silently=False,
                )
                except BadHeaderError :
                    return 
                instance.has_withdrawn=False
                instance.save()
                ac = get_object_or_404(Wr,account=instance) # delete the withdraw request instance
                ac.delete()
            if instance.withdraw_failed:
                try:
                    print('sending withdraw failed email',to_email)
                    send_mail(
                'TASKfindr Withdrawal failed ',
                f'Hi,{instance.owner.username} your withdrawal request has beed denied,check if your mpesa phone number matches the one in your profile or call us on 07..........',
                from_email,
                [to_email],
                fail_silently=False,
                )
                except BadHeaderError :
                    return
                instance.withdraw_failed=False
                instance.save()
                ac = get_object_or_404(Wr,account=instance)# delete the withdraw request instance
                ac.delete()
        else:
            pass


""" this is for me to remember (it should live in a dotenv file)
STEPS FOR THE WHOLE SHIT
1. join -> the site makes a profile then a cash account deleting either does not affect the orther

2. activate -> when you submit the mpesa code the site manager verifies the code and saves the account

3. track refferal -> the site recieves the save signal then starts the logic to trace the refferal

4. withdraw -> if yu try when you havnt got the cash it will just say no, otherwise it creates a withdraw request model instance
               which site managers use to know who wants to withdraw. luckily when site managers save your account again while confirming
               that you can or cannot withdraw that withdraw request will be deleted so you can make another one.

5.  send email -> we send you an email during 3 occassions when you join,when you fail to withdraw & when you successfully withdraw
                the emails correspond to the action you take they are triggered when the cash account is saved so be carefull while 
                saving anything in the admin since most logic is called after you save a model.

"""