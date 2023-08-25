from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path('auth/', obtain_auth_token,name="authtokens"),
    path('allblogs/', views.Bloglistview.as_view(), name='allblogs'),
    path('blog/<int:pk>/', views.Blogdetailview.as_view(), name='blogpost-detail'),
    path('myblogs/', views.MyBlogs.as_view(), name='blogpost-mine'),
    path('reactions/<int:pk>/', views.Postreactionview.as_view(), name='Postreaction-single'),
    path('youtube/', views.youtube_oauth_callback, name='youtube_oauth_callback'),

]