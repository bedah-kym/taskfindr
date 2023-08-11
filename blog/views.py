from django.shortcuts import get_list_or_404, render,get_object_or_404,redirect
from django.urls import reverse
from .models import blogpost as post,Postreaction 
from django.contrib.auth.models import User
from users.models import Cashaccount
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

class postlistview(LoginRequiredMixin, ListView):
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
        return context
    
    

class postdetailview(LoginRequiredMixin,DetailView):
    model=post
    template_name='blog/post-detail.html'
    context_object_name= 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likes,dislikes = Postreaction.total_reactions(self.get_object())
        reactions ={
            "likes":likes,
            "dislikes":dislikes
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
    fields=['title','content','spaces']
    template_name='blog/post_form.html'

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def is_unique_content(self,form):
        """ id like to ensure that the content posted is unique so users dont repost the same shit
        just checking the title is not worth it but we need to use an AI service.so before a post
        is saved the test func will call this func send it to the AI ,parse the result and take action
        """
        pass

    def test_func(self):
        """ call is_unique_content if true, check the current date aginst the date of the last post by the user
        if the date is the same as current date then return false
        """
        user = self.request.user
        blog = post.objects.filter(author=user).last()
        if blog :
            today = timezone.now().day
            this_month = timezone.now().month
            posted_month = blog.date_posted.month
            posted_day = blog.date_posted.day
            if this_month == posted_month:
                if today == posted_day:
                    return False
                else:
                    return True
            elif this_month > posted_month:
                return True
            else:
                return False
        else:
            return True
        
       

class postupdateview(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model=post
    template_name= 'blog/post_form.html'
    fields=['title','content']

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
    
def likepost(request,pk):
    fan=request.user
    blog=post.objects.get(pk=pk)
    if Postreaction.can_react(request,blog):        
        Postreaction.objects.create(fan=fan,post=blog,reaction="like")
    else:
        Postreaction.change_reaction(request,blog)

    return redirect(reverse('post_detail',kwargs={"pk":blog.id}))

def dislikepost(request,pk):
    fan=request.user
    blog=post.objects.get(pk=pk)
    if Postreaction.can_react(request,blog):        
        Postreaction.objects.create(fan=fan,post=blog,reaction="dislike")
    else:
        Postreaction.change_reaction(request,blog)
    return redirect(reverse('post_detail',kwargs={"pk":blog.id}))

def tasklistview(request):
    return render(request,'blog/tasklist.html',{})

def about_view(request):
    return render(request,'blog/about.html',{})

def termsview(request):
    return render(request,'blog/activation_success.html',{})
