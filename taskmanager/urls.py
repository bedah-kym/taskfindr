from django.urls import path
from .views import (
    CreateJobOffer,
    JobOfferUpdate,
    MilestoneCRUDView,
    BidCRUDView,
    AcceptOrDeclineBidView
)

urlpatterns=[
    path('joboffer/<int:pk>',CreateJobOffer.as_view(),name='new-joboffer'),
    path('updateoffer/<int:pk>/',JobOfferUpdate.as_view(),name='update-offer'),
    path('milestone/create/<int:pk>/', MilestoneCRUDView.as_view(), name='new-milestone'),
    path('milestone/update/<int:pk>/<int:milestone_id>/', MilestoneCRUDView.as_view(), name='milestone_update'),
    path('milestone/delete/<int:pk>/<int:milestone_id>/', MilestoneCRUDView.as_view(), name='milestone_delete'),
    path('offerbid/create/<int:pk>/', BidCRUDView.as_view(), name='new-bid'),
    path('offerbid/update/<int:pk>/<int:bid_id>/', BidCRUDView.as_view(), name='bid_update'),
    path('offerbid/delete/<int:pk>/<int:bid_id>/', BidCRUDView.as_view(), name='bid_delete'),
    path('offerbid/<int:bid_id>/<str:response>/',AcceptOrDeclineBidView , name='bid_response'),
    
]