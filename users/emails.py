#all emails to be sent should live in one place
from templated_email import send_templated_mail
from django.http import Http404
from django.shortcuts import get_object_or_404


def send_info_email(instance,event):
    to_email = instance.owner.email
    from_email = 'taskfindrlimited@gmail.com'
    username = instance.owner.username
    print(f'sending {event}email to',to_email)
    if event == "created":
        content=f"hello {username} we are pleased to have you in our community please open a cash account by depositing a minimum of a hundred shilings to paybill 1234 ac no: 4568135154 and start earning .Also tell a friend."
    elif event == "success":
        content = f'Hi,{username} your withdrawal request is successfull, we will send you the amount on your phone number shortly.'  
    elif event == "failed":
        content = f'Hi{username} your withdrawal request has beed denied,check if your mpesa phone number matches the one in your profile and the mpesa code submitted it correct.Thank you',
    else:
        content = f'sorry we are experiencing a technical glitch in our email system please ignore this email '
    send_templated_mail(
            template_name='welcome',
            from_email=from_email,
            recipient_list=[to_email],
            context={
                'username':username,
                'content':content  
            },
            fail_silently=False,
        )   
    
def warning_email(user,event):
    """these emails are for when the admin checks if your account is active so you will be warned or reposessed
    """
    try:
        to_email = user.email
        from_email = 'taskfindrlimited@gmail.com'
        print(f'sending {event}email to',to_email)
        if event == "warn":
            content=f'Hi,{user.username} you have been away from taskfinder for a while.Come back and check out our new offers and earning points'
        else:
            content = f'Hi,{user.username} you have been away from taskfinder for too long unfortunately we can  no longer keep your account active'
        send_templated_mail(
            template_name='welcome',
            from_email=from_email,
            recipient_list=[to_email],
            context={
                'username':user.username,
                'content':content  
            },
            fail_silently=False,
        )   
    except Http404:
        pass