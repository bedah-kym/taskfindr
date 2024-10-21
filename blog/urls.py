from django.urls import path 
from .views import (
    about_view,
    termsview,
    postlistview,
    postdetailview,
    postcreateview,
    postupdateview,
    postdeleteview,
    userpostlistview,
    categorypostlistview,
    likepost,
    dislikepost,
    wheelspinview,
    social_boost
    
)

urlpatterns=[
    path('',postlistview.as_view(),name='home'),
    path('spin-the-wheel/',wheelspinview,name='wheelspin'),
    path('post/new/',postcreateview.as_view(),name='new-post'),
    path('post/<int:pk>/',postdetailview.as_view(),name='post_detail'),
    path('user/<str:username>/',userpostlistview.as_view(),name='user_post'),
    path('category/<str:spaces>/',categorypostlistview.as_view(),name='spaces_list'),
    path('post/<int:pk>/update/',postupdateview.as_view(),name='post_update'),
    path('post/<int:pk>/delete/',postdeleteview.as_view(),name='post_delete'),
    path('likepost/<int:pk>/',likepost,name='like'),
    path('dislikepost/<int:pk>/',dislikepost,name='dislike'),
    path('about/',about_view,name='about'),
    path('social-boost/',social_boost,name='social'),
    path('terms_and_conditions/',termsview,name='terms'),
    
]