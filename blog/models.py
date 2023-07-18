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
    reaction = models.ManyToManyField(User,through="Postreaction",related_name="blogpost_reactions")
    
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
    
class Postreaction(models.Model):
    fan = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(blogpost,on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10)

    class Meta:
        verbose_name ="Postreaction"
        verbose_name_plural = "Postreactions"

    def __str__(self):
        return self.reaction

    def get_absolute_url(self):
        return reverse("Postreaction_detail", kwargs={"pk": self.pk})
    
    def can_react(request,post):
        reactions = Postreaction.objects.filter(post=post,fan=request.user)
        #returns alist if the list has more than one reaction return
        if len(reactions )< 1 :
            return True
        elif len(reactions)>1:
            return False
        
    def change_reaction(request,post):
        reactions = Postreaction.objects.filter(post=post,fan=request.user)
        reactions.delete()

    def total_reactions(request,post):   
        likes = Postreaction.objects.filter(post=post,reaction="like")
        dislikes = Postreaction.objects.filter(post=post.id,reaction="dislike")
        total_likes = likes.count()
        total_dislikes = dislikes.count()
        return(total_likes,total_dislikes)
        