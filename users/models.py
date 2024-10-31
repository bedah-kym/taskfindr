from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator
from blog.models import blogpost,WheelSpin

class profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default ='default.jpg', upload_to ='profile_pics')
    bio = models.TextField(default=True)
    preference = models.TextField(default=True)
    level= models.IntegerField(default=1)
    phone_number = models.IntegerField(default=0)
    reffered_by = models.CharField(max_length=50,default=None,null=True)
    leveled_up = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    work_done = models.ManyToManyField(blogpost,related_name="jobs_done")
    
    def  __str__(self):
        return  f'{self.user.username} Profile'

    def verifiy_user(self,user):
        account=self.objects.filter(user=user)
        if account.is_verified:
            return True
        else:
            account.is_verified=True
            
    def unverify_user(self,user):
        account=self.objects.filter(user=user)
        if account.is_verified:
            account.is_verified=False
        return False
              
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img= Image.open(self.image.path)
        if img.width> 300 or img.height>300:
            outputsize=(300,300)
            img.thumbnail(outputsize)
            img.save(self.image.path)

class Cashaccount(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=10,default=None,null=True,validators=[RegexValidator(r"^[0-9|A-Z]{10}$",'invalid code')])
    level_bonus = models.IntegerField(default=0)
    refferals = models.ManyToManyField(profile,default=None)
    amount = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=False)
    has_withdrawn = models.BooleanField(default=False)
    withdraw_failed = models.BooleanField(default=False)

    def get_refferal_cash(self):
        total = self.refferals.count()
        total*=100
        return total
    
    def get_level_bonus(self):#if ur, say level 2 and above you get a bonus of your level multiplied by 100 (2*100)
        bonus=0
        if self.amount >= 200:
            user_level = (self.amount//100)
            bonus = (user_level-1)*100
        return bonus
    
    def get_total_cash(self,user):
        bonus= self.get_level_bonus()
        posts = blogpost.objects.filter(author=user)
        spins = WheelSpin.objects.filter(spinner=user)
        spincash = 0
        for spin in spins:
            spincash += spin.value
        total=0
        for post in posts:
            cash=post.price_offer
            total+=cash
        taskcash=self.get_refferal_cash()
        total+=taskcash
        total+=bonus
        total +=spincash
        return total

    def get_total_tasks(self,user): 
        posts = blogpost.objects.filter(author=user)
        spins = WheelSpin.objects.filter(spinner=user)
        p=posts.count()
        s=spins.count()
        tasks={
            "posts":p,
            "spins":s
        }
        return tasks
    
    def withdraw_cash(self):
        self.refferals.delete().all()
        self.mpesa_code.delete()

    def reposess_account(self,user):
        ac = self.objects.filter(owner=user).first()
        if ac:
            ac.is_valid=False
            return True
        return False

    
    def __str__ (self):
        return f'{self.owner} with ksh {self.get_total_cash(self.owner)} has {self.refferals.count()} refferal(s)'

class Withdrawrequest(models.Model):
    account = models.ForeignKey(Cashaccount, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return f"{self.account.owner.username} requested to withdraw on month {self.request_date.month} ,{self.request_date.day}th "

class Leveluprequest(models.Model):
    user_profile = models.ForeignKey(profile,on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    mpesa_code = models.CharField(max_length=10,default=None,null=True,validators=[RegexValidator(r"^[0-9|A-Z]{10}$",'invalid code')])
    
    def __str__ (self):
        return f"{self.user_profile.user.username} requested to level up on month{self.request_date.month}, {self.request_date.day}th "

