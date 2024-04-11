from django.db import models
import requests
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from django.utils.html import strip_tags
from django.template.defaultfilters import Truncator
from django.core.validators import FileExtensionValidator
CATEGORY_CHOICES = [
    ("MUSIC AND ART", "Music and Art"),
    ("CYBER-SECURITY", "Ethical Hacking"),
    ("FOOD AND LIFESTYLE", "Food and life"),
    ("LIFE HACKS AND JOBS", "Money and Jobs"),
    ("PROGRAMMING AND DATA SCIENCE", "Coding"),
]

class blogpost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    excerpt = models.TextField(max_length=300)
    image = models.ImageField(
        upload_to='blog_images/', 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True, blank=True)
    ext_url= models.URLField(null=True,default=None)
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
    def save(self, *args, **kwargs):
        if self.image is not None:
            response = requests.get(self.image)
            if response.status_code == 200:
                # Open the image using Pillow for additional processing if needed
                 # Convert the binary data to a file-like object
                img = BytesIO(response.content)
                
                # Optionally perform image processing or resizing
                # img = img.resize((width, height), Image.ANTIALIAS)

                # Save the image to the model's ImageField
                self.image.save(f"{self.title}_image.jpg", File(img), save=False)
            # Automatically generate excerpt from content
        if not self.excerpt:
            # Strip HTML tags and truncate to get a sample paragraph
            plain_text_content = strip_tags(self.content)
            self.excerpt = Truncator(plain_text_content).words(50)  # Adjust the word count as needed

        super().save(*args, **kwargs)

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
        return f"{self.reaction} for post{self.post}"

    def get_absolute_url(self):
        return reverse("Postreaction_detail", kwargs={"pk": self.pk})
    
    def can_react(request,post):
        all_reactions = Postreaction.objects.filter(post=post,fan=request.user)
        reactions=[]
        #returns alist if the list has more than one reaction return
        for react in all_reactions:
            # delete all view reactions, if you dont you cant like/dislike a post you have viewed since it is a reaction
            if react.reaction != "view":
                reactions.append(react)
        if len(reactions )< 1 :
            return True
        elif len(reactions)>1:
            return False
        
    def change_reaction(request,post):
        reactions = Postreaction.objects.filter(post=post,fan=request.user)
        reactions.delete()

    def total_reactions(post):   
        likes = Postreaction.objects.filter(post=post,reaction="like")
        dislikes = Postreaction.objects.filter(post=post,reaction="dislike")
        total_likes = likes.count()
        total_dislikes = dislikes.count()
        return(total_likes,total_dislikes)
    
    def total_views(request,post):
        blog=post
        views = Postreaction.objects.filter(post=blog,fan=request.user,reaction="view")
        all_views = Postreaction.objects.filter(post=blog,reaction="view").count()
        if views:   
            return all_views
        else:    
            Postreaction.objects.create(fan=request.user,post=blog,reaction="view")
            return all_views

   


        
class WheelSpin(models.Model):
    spin_date = models.DateTimeField(auto_now_add=True)
    spinner = models.ForeignKey(User,on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self) -> str:
        return (f"{self.spinner} on {self.spin_date}")

    def can_spin(user):
        try:
            last_spin = WheelSpin.objects.filter(spinner=user).last()
        except Http404:
            return True
        if last_spin:
            now = timezone.now().day
            last = last_spin.spin_date.day
            if now == last:
                return False
            else:
                return True
        else:
            return True
    