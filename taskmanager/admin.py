from django.contrib import admin
from .models import JobOffer,OfferBids,OfferMilestones

admin.site.register(JobOffer)
admin.site.register(OfferBids)
admin.site.register(OfferMilestones)

