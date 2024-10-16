from django.db import models
from blog.models import blogpost as jobpost
from users.models import profile

class JobOffer(models.Model):
    class Meta:
        verbose_name ="job offers"
        verbose_name_plural = "job offers"

    STATUS_CHOICES = [
        ("ASSIGNED", "assigned"),
        ("OPEN", "open"),
        ("COMPLETED", "complete"),
        ("REVIEW", "review"),     
    ]
    job = models.ForeignKey(jobpost, on_delete=models.CASCADE)
    milestones = models.ManyToManyField('OfferMilestones', related_name="job_milestones",blank=True)
    accept_offer = models.BooleanField(default=False)
    bids = models.ManyToManyField('OfferBids', related_name="job_bids",blank=True)
    time_limit = models.DurationField()
    job_status = models.CharField(choices=STATUS_CHOICES, default="OPEN", max_length=20)
    
    def __str__(self):
        return(f" job offer details for : {self.job.title}")
        
class OfferBids(models.Model):
    class Meta:
        verbose_name ="offer bids"
        verbose_name_plural = "offer bids"

    joboffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    cashbid = models.IntegerField(default=0)
    bidder = models.ForeignKey(profile, on_delete=models.CASCADE)

class OfferMilestones(models.Model):
    class Meta:
        verbose_name ="offer milestones"
        verbose_name_plural = "offer milestones"

    MILESTONE_TAGS = [
        ("REQUIRED", "required"),
        ("OPTIONAL", "optional"),
        ("SUGGESTION", "suggestion")
    ]
    content = models.TextField(max_length=500)
    joboffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    tags = models.CharField(choices=MILESTONE_TAGS, max_length=30, null=True, default=None)
    extra_cash = models.IntegerField(default=0, null=True)
