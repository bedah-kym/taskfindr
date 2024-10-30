from dirtyfields import DirtyFieldsMixin
from django.db import models
from blog.models import blogpost 
from users.models import profile
from django.utils import timezone
from datetime import timedelta

class JobOffer(DirtyFieldsMixin,models.Model):
    class Meta:
        verbose_name ="job offers"
        verbose_name_plural = "job offers"

    STATUS_CHOICES = [
        ("ASSIGNED", "assigned"),
        ("OPEN", "open"),
        ("COMPLETED", "complete"),
        ("REVIEW", "review"),     
    ]
    job = models.ForeignKey(blogpost,on_delete=models.CASCADE,related_name='job_offer')
    milestones = models.ManyToManyField('OfferMilestones', related_name="job_milestones",blank=True)
    bids = models.ManyToManyField('OfferBids', related_name="job_bids",blank=True)
    time_limit = models.DurationField()
    job_status = models.CharField(choices=STATUS_CHOICES, default="OPEN", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.pk and 'time_limit' in self.get_dirty_fields():
            # Update the `created_at` timestamp when `time_limit` changes
            self.created_at = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def time_left(self):
        """Calculate time remaining until the task expires."""
        if self.time_limit:
            expiration_time = self.created_at + self.time_limit
            remaining_time = expiration_time - timezone.now()
            return remaining_time if remaining_time > timedelta(0) else timedelta(0)  # Return 0 if time is up
        return None  # 
    
    def __str__(self):
        return(f" job offer details for : {self.job.title}")
        
class OfferBids(models.Model):
    class Meta:
        verbose_name ="offer bids"
        verbose_name_plural = "offer bids"
    BID_STATUS = [
        ("WAITING",'waiting'),
        ("ACCEPTED",'accepted'),
        ("DECLINED",'declined')
    ]
    
    joboffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    cashbid = models.IntegerField(default=0)
    bidder = models.ForeignKey(profile, on_delete=models.CASCADE)
    bid_status = models.CharField(choices=BID_STATUS,max_length=20,default="waiting")

class OfferMilestones(models.Model):
    class Meta:
        verbose_name ="offer milestones"
        verbose_name_plural = "offer milestones"

    MILESTONE_TAGS = [
        ("REQUIRED", "required"),
        ("OPTIONAL", "optional"),
        ("SUGGESTION", "suggestion")
    ]
    heading = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    joboffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    tags = models.CharField(choices=MILESTONE_TAGS, max_length=30, null=True, default=None)
    extra_cash = models.IntegerField(default=0, null=True)
    
    def __str__(self):
        return(f"milestone for: {self.joboffer}")
