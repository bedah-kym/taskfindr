from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import blogpost as post,Postreaction ,WheelSpin
from django.contrib.auth.models import User
from users.models import Cashaccount
from django.utils import timezone
from .plagiarism_detection import calculate_similarity
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from API.news_api import parse_results

from .forms import CustomPostForm
from django.shortcuts import redirect


def error_404_view(request, exception):
	return render(request, 'blog/404.html')

def error_403_view(request, exception):
	return render(request, 'blog/403_csrf.html')

@login_required
def social_boost(request):
    return render(request,'blog/social.html')



class postlistview(LoginRequiredMixin,UserPassesTestMixin, ListView):
   
    model= post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=10

    def get_context_data(self, **kwargs):
        user = self.request.user
        total_users = User.objects.count()*100
        account = Cashaccount.objects.get(owner=user)
        reffs=account.refferals.count()
        amount= account.get_total_cash(user)
        tasks = account.get_total_tasks(user)
        level = account.get_level_bonus()
        context = super().get_context_data(**kwargs)
       
        new={
            "reffs":reffs,
            "tasks":tasks,
            "cash":amount,
            "level":level,
            "total_users":total_users
        }
        context.update(new) 
        #print(context["posts"][0].content)
        return context
    
    def test_func(self):
       if self.request.user.is_active:
           return True
       else:
           return False

class postdetailview(LoginRequiredMixin,DetailView):
    model=post
    template_name='blog/post-detail.html'
    context_object_name= 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likes,dislikes = Postreaction.total_reactions(self.get_object())
        views= Postreaction.total_views(self.request,self.get_object())
        reactions ={
            "likes":likes,
            "dislikes":dislikes,
            "views": views
        }
        context.update(reactions)
        return context
        
class userpostlistview(LoginRequiredMixin,ListView):
    model= post
    template_name='blog/user_posts.html'
    context_object_name='posts'
    paginate_by=10

    def get_queryset(self):
        user = get_object_or_404(User, username= self.kwargs.get('username'))
        return  post.objects.filter(author=user).order_by('-date_posted')
    
class categorypostlistview(LoginRequiredMixin,ListView):
    model= post
    template_name='blog/category_posts.html'
    context_object_name='posts'
    paginate_by=10

    def get_queryset(self):
        category = self.kwargs.get('spaces')
        return  post.objects.filter(spaces=category).order_by('-date_posted')

class postcreateview(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model=post
    form_class = CustomPostForm
    template_name='blog/post_form.html'

    def form_valid(self,form):
        form.instance.author=self.request.user
        content = form.instance.content
        if self.is_unique(content): 
            return super().form_valid(form)
        else:
            return HttpResponse('YOUR CONTENT IS NOT ORIGINAL, PLEASE REVISE YOUR CONTENT AND REPOST')
    
    def is_unique(self,content):
        # Check for plagiarism against existing posts using nltk lib
        existing_posts = post.objects.all()
        for singlepost in existing_posts:
            similarity = calculate_similarity(content, singlepost.content)
            if similarity > 0.7:  # Adjust the threshold as needed
                # Flag the post as potential plagiarism or take appropriate action
                messages.warning(self.request,f"Potential plagiarism detected: Similarity with '{singlepost.title}': {similarity}")
                return False
        return True
        

    def test_func(self):
        """ call is_unique_content if true, check the current date aginst the date of the last post by the user
        if the date is the same as current date then return false
        """
        user = self.request.user
        if user.is_superuser:
            return True
        blog = post.objects.filter(author=user).last()   
        if blog:
            today = timezone.now().day
            this_month = timezone.now().month
            posted_month = blog.date_posted.month
            posted_day = blog.date_posted.day

            if this_month == posted_month:
                if today == posted_day:
                    return False
                else:
                    return True
            return True
        else:
            return True
       
class postupdateview(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model=post
    template_name= 'blog/post_form.html'
    form_class = CustomPostForm

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

class postdeleteview(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model=post
    template_name= 'blog/post_confirm_delete.html'
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

def get_news(request,**kwargs):
    all_posts_info = parse_results(kwargs['category'])
    # each post_info dictionary represents a single post
    for post_info in all_posts_info:
        post.objects.create(
            title=post_info['title'],
            content=post_info['content'],
            date_posted=timezone.now(),
            author=User.objects.get(username='blogadmin'),
            spaces=post_info['space'],
            image=post_info['images'],
            ext_url=post_info['mainlink'],
            value=20
        )

    return redirect('profile')
    
@login_required  
def likepost(request,pk):
    fan=request.user
    blog=post.objects.get(pk=pk)
    if Postreaction.can_react(request,blog):        
        Postreaction.objects.create(fan=fan,post=blog,reaction="like")
    else:
        Postreaction.change_reaction(request,blog)

    return redirect(reverse('post_detail',kwargs={"pk":blog.id}))

@login_required
def dislikepost(request,pk):
    fan=request.user
    blog=post.objects.get(pk=pk)
    if Postreaction.can_react(request,blog):        
        Postreaction.objects.create(fan=fan,post=blog,reaction="dislike")
    else:
        Postreaction.change_reaction(request,blog)
    return redirect(reverse('post_detail',kwargs={"pk":blog.id}))

@login_required
def wheelspinview(request):
    #first check if the user can spin then get the data
    spinuser = request.user
    if WheelSpin.can_spin(spinuser):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            post_data= json.load(request)['post_data']     
            data = {
                'my_data':post_data,
            }
            options=[10,20,30,40,50,60]
            if data['my_data'] in options:
                WheelSpin.objects.create(spinner=spinuser,spin_date=timezone.now(),value=data['my_data'])
                messages.warning(request,f"congrats we have added {data['my_data']}/= to your account ") 
                
    else:
        messages.warning(request,"sorry you can only spin the wheel once a day !") 
        return redirect('profile')

    return render(request,'blog/wheel.html')

def about_view(request):
    return render(request,'blog/about.html',{})

def termsview(request):
    return render(request,'blog/activation_success.html',{})


