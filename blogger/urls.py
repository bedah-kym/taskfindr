"""blogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog.views import (
    about_view,
    postlistview,
    postdetailview,
    postcreateview,
    postupdateview,
    postdeleteview,
    userpostlistview,
    categorypostlistview
)
from users.views import (
    register_view,
    profile_view,
    Cashaccountupdate,
    Cashaccountdelete,
    withdrawalrequest,
)
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',postlistview.as_view(),name='home'),
    path('post/new/',postcreateview.as_view(),name='new-post'),
    path('post/<int:pk>/',postdetailview.as_view(),name='post_detail'),
    path('user/<str:username>/',userpostlistview.as_view(),name='user_post'),
    path('category/<str:spaces>/',categorypostlistview.as_view(),name='spaces_list'),
    path('post/<int:pk>/update/',postupdateview.as_view(),name='post_update'),
    path('post/<int:pk>/delete/',postdeleteview.as_view(),name='post_delete'),
    path('register/<str:code>/',register_view,name='register'),
    path('withdraw/',withdrawalrequest,name='withdrawal_request'),
    path('profile/',profile_view,name='profile'),
    path('account-activation/<int:pk>/',Cashaccountupdate.as_view(),name='activation'),
    path('delete-account/<int:pk>/',Cashaccountdelete.as_view(),name='delete_account'),
    path('login/',views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',views.LogoutView.as_view(template_name='blog/landing-page.html'),name='logout'),
    path('password-reset/',views.PasswordResetView.as_view(template_name='blog/password_reset.html'),name='password_reset'),
    path('password-reset-done/',views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'),name='password_reset_complete'),
    path('about/',about_view,name='about'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
