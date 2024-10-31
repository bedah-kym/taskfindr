from django.urls import path
from django.contrib.auth import views

from .views import (
    register_view,
    profile_view,
    Cashaccountupdate,
    Cashaccountdelete,
    withdrawalrequest,
    levelup,
    admincheckaccounts,
)


urlpatterns =[
    path('register/<str:code>/',register_view,name='register'),
    path('withdraw/',withdrawalrequest,name='withdrawal_request'),
    path('level_up/',levelup,name='level_up'),
    path('profile/',profile_view,name='profile'),
    path('account-activation/<int:pk>/',Cashaccountupdate.as_view(),name='activation'),
    path('check-accounts/',admincheckaccounts,name='check_accounts'),
    path('delete-account/<int:pk>/',Cashaccountdelete.as_view(),name='delete_account'),
     path('login/',views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',views.LogoutView.as_view(template_name='blog/landing-page.html'),name='logout'),
    path('password-reset/',views.PasswordResetView.as_view(template_name='blog/password_reset.html'),name='password_reset'),
    path('password-reset-done/',views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'),name='password_reset_complete'),
    
    
]