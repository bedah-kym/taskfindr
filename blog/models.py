from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

CATEGORY_CHOICES = [
    ("MUSIC AND ART", "Music and Art"),
    ("CYBER-SECURITY", "Ethical Hacking"),
    ("FOOD AND LIFESTYLE", "Food and life"),
    ("LIFE HACKS AND JOBS", "Money and Jobs"),
    ("PROGRAMMING AND DATA SCIENCE", "Coding"),
]

class blogpost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    spaces = models.CharField(choices=CATEGORY_CHOICES,max_length=30,null=False,default=None)
    value = models.IntegerField(default=20)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})

    def is_task_valid(self):
        """ check the current time aginist the time of the last post by the user
        if the time is the same as current time then return false
        """
        user = self.request.user
        last_blog = blogpost.objects.get(author=user)
        now = timezone.now().day
        last = last_blog.date_posted.day
        if now == last:
            return False
        else:
            return True

    def __str__(self):
        return f"{self.title} by {self.author}"
    
