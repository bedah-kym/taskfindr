from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect
from.models import JobOffer
from blog.models import blogpost
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import JobOfferForm, OfferBidsForm, OfferMilestonesForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

class CreateJobOffer(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model=JobOffer
    form_class = JobOfferForm
    template_name = 'blog/jobofferform.html'
    context_object_name='offerform'
    success_url=reverse_lazy('profile')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        postid = self.kwargs.get('pk')
        
        # Set the job field queryset to the specific post
        form.fields['job'].queryset = blogpost.objects.filter(pk=postid)
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offerform'] = self.get_form(self.get_form_class()) 
        return context
    
    def form_valid(self, form):
        job = form.cleaned_data.get('job')
        offerexists = JobOffer.objects.filter(job=job).exists()
        
        if offerexists:
            messages.warning(self.request, "You already have an offer for this job!")
            return HttpResponseRedirect(self.success_url) 
        
        return super().form_valid(form)
    
    def test_func(self) -> bool:
        #ill think of a test for this
        if self.request.user:
            return True
        return False
    
class JobOfferUpdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = JobOffer
    template_name = 'blog/jobofferform.html'
    form_class = JobOfferForm
    context_object_name = 'offerform'
    success_url= '/'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        joboffer = self.get_object()
        
        # Set the job field queryset to the specific post associated with the offer
        form.fields['job'].queryset = blogpost.objects.filter(pk=joboffer.job.pk)
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offerform'] = self.get_form(self.get_form_class()) 
        return context
    
    def test_func(self):
        offer = self.get_object()
        if self.request.user == offer.job.author:
            return True
        return False  
    
class JobOfferDelete(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model=JobOffer
    template_name = 'blog/offerdelete.html'
    success_url = '/'

    def test_func(self):
        offer = self.get_object()
        if self.request.user == offer.job.author:
            return True
        return False    

class JobOfferList(LoginRequiredMixin,ListView):
    model= JobOffer
    template_name='blog/joboffer_list.html'
    context_object_name='offers'
    #paginate_by=10

  