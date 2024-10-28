from django import forms
from .models import JobOffer, OfferBids, OfferMilestones

class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = ['job','job_status', 'time_limit']
        widgets = {
            'job': forms.Select(attrs={
                'class': 'form-control',
            }),
            'job_status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'time_limit': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter in format: hours:mins:sec',
            })
        }


class OfferBidsForm(forms.ModelForm):
    class Meta:
        model = OfferBids
        fields = ['joboffer','cashbid']
        widgets = {
            'joboffer': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cashbid': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter cash bid amount',
            }),
            
        }


class OfferMilestonesForm(forms.ModelForm):
    class Meta:
        model = OfferMilestones
        fields = ['joboffer','heading','content', 'tags', 'extra_cash']
        widgets = {
            'joboffer': forms.Select(attrs={
                'class': 'form-control',
            }),
            'heading':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'milestone heading'
                }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the milestone',
            }),
            'tags': forms.Select(attrs={
                'class': 'form-control',
            }),
            'extra_cash': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Extra cash for this milestone',
            }),
        }

