from django.urls import path
from .views import (
    CreateJobOffer,
    JobOfferDelete,
    JobOfferList,
    JobOfferUpdate
)

urlpatterns=[
    path('joboffer/<int:pk>',CreateJobOffer.as_view(),name='new-joboffer'),
    path('deleteoffer/<int:pk>',JobOfferDelete.as_view(),name='delete-offer'),
    path('updateoffer/<int:pk>',JobOfferUpdate.as_view(),name='update-offer'),
]