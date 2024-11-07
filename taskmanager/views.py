from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from.models import JobOffer ,OfferMilestones, OfferBids
from blog.models import blogpost
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import JobOfferForm, OfferMilestonesForm, OfferBidsForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    View,
    CreateView,
    UpdateView,
    DeleteView
)

class CreateJobOffer(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model=JobOffer
    form_class = JobOfferForm
    template_name = 'blog/jobofferform.html'
    context_object_name='offerform'
    
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
        
        if 'save' in self.request.POST:
            self.object = form.save()
            return redirect('new-milestone',pk=self.object.pk)
        
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
    

class MilestoneCRUDView(LoginRequiredMixin, View):
    model = OfferMilestones
    form_class = OfferMilestonesForm
    success_url = reverse_lazy('profile')
    template_name = 'blog/milestonesform.html'

    def get_form(self, offer_id=None, milestone=None):
        form = self.form_class(instance=milestone)
        if offer_id:
            form.fields['joboffer'].queryset = JobOffer.objects.filter(pk=offer_id)
        return form

    def get_job_offer(self, offer_id):
        """Retrieve JobOffer and ensure the user is the owner."""
        joboffer = get_object_or_404(JobOffer, pk=offer_id)
        if joboffer.job.author != self.request.user:
            return None  # User is not the owner
        return joboffer

    def get(self, request, *args, **kwargs):
        offer_id = self.kwargs.get('pk')
        joboffer = self.get_job_offer(offer_id)
        if not joboffer:
            return self.handle_no_permission()

        milestone = None
        if 'milestone_id' in kwargs:
            milestone = get_object_or_404(self.model, id=kwargs['milestone_id'])
        
        form = self.get_form(offer_id, milestone)
        context = {'form': form, 'offer_id': offer_id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        offer_id = self.kwargs.get('pk')
        joboffer = self.get_job_offer(offer_id)
        if not joboffer:
            return self.handle_no_permission()

        milestone = None
        if 'milestone_id' in kwargs:
            milestone = get_object_or_404(self.model, id=kwargs['milestone_id'])
            if 'delete' in request.POST:
                milestone.delete()
                return redirect(self.success_url)
            else:
                form = self.form_class(request.POST, instance=milestone)
        else:
            form = self.form_class(request.POST)

        form.fields['joboffer'].queryset = JobOffer.objects.filter(pk=offer_id)
        
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.joboffer = joboffer
            milestone.save()
            joboffer.milestones.add(milestone)
            if "finish" in request.POST :
                return HttpResponseRedirect(self.success_url)

        context = {'form': form}
        return render(request, self.template_name, context)
    
class BidCRUDView(LoginRequiredMixin,View):
    model = OfferBids
    form_class = OfferBidsForm
    template_name ='blog/jobbidform.html'
    success_url = reverse_lazy('profile')
    
    def get_form(self, offer_id=None, offerbid=None):
        form = self.form_class(instance=offerbid)
        job = JobOffer.objects.get(pk=offer_id).job
        post_price = blogpost.objects.get(pk=job.id).price_offer
        if offer_id:
            form.fields['joboffer'].queryset = JobOffer.objects.filter(pk=offer_id)
            form.initial['cashbid'] = post_price
        return form

    def get_job_offer(self, offer_id):
        joboffer = get_object_or_404(JobOffer, pk=offer_id)
        return joboffer

    def get_bid(self, bid_id):
        offerbid = get_object_or_404(self.model, id=bid_id)
        if offerbid.bidder != self.request.user.profile:  
            raise self.handle_no_permission
        return offerbid

    def get(self, request, *args, **kwargs):
        offer_id = self.kwargs.get('pk')
        offerbid = None
        if 'bid_id' in kwargs:
            offerbid = self.get_bid(kwargs['bid_id'])  
        
        form = self.get_form(offer_id, offerbid)
        context = {'bidform': form, 'offer_id': offer_id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        offer_id = self.kwargs.get('pk')
        joboffer = self.get_job_offer(offer_id)
        offerbid = None
        if 'bid_id' in kwargs:
            offerbid = self.get_bid(kwargs['bid_id']) 
            if 'delete' in request.POST:
                offerbid.delete()
                return redirect(self.success_url)
            else:
                form = self.form_class(request.POST, instance=offerbid)
        else:
            form = self.form_class(request.POST)

        form.fields['joboffer'].queryset = JobOffer.objects.filter(pk=offer_id)
        
        bidexists = OfferBids.objects.filter(joboffer=joboffer,bidder=request.user.profile).exists()
        if bidexists == False:
            if form.is_valid():
                offerbid = form.save(commit=False)
                offerbid.bidder = request.user.profile
                offerbid.joboffer = joboffer 
                offerbid.save()
                joboffer.bids.add(offerbid)
                return HttpResponseRedirect(self.success_url)

            context = {'bidform': form}  
            return render(request, self.template_name, context)
        else:
            messages.warning(request,"you have already bid for this job")
            return redirect(self.success_url)
        
@login_required
def AcceptOrDeclineBidView(request,bid_id,response):
    bid = OfferBids.objects.get(pk=bid_id)
    if bid.joboffer.job.author == request.user:
        if response == "Accept":
            if bid.bid_status == "WAITING" or bid.bid_status == "waiting":
                bid.bid_status = 'ACCEPTED'
                bid.save()
                contract = bid.joboffer.job
                contract.assigned_to = bid.bidder.user
                contract.save()
                offer = bid.joboffer
                offer.job_status = "ASSIGNED"
                offer.save() 
                messages.success(request,f"you have accepted {bid.bidder}s bid proceed to work-area")
                return redirect('profile')
            else:
                messages.warning(request,f'you have already responded to this bid with "{bid.bid_status}"')
                return redirect('profile')
        else:
            if response == "Decline":
                if bid.bid_status == "WAITING"or bid.bid_status == "waiting":
                    bid.bid_status ='DECLINED' 
                    bid.save()
                    return redirect('profile')  
                else:
                    messages.warning(request,'you have already responded to this bid')   
                    return redirect('profile')
    else:
        request.handle_no_permission()
    