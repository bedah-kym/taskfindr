
from django import forms
from .models import blogpost,JobRating


class CustomPostForm(forms.ModelForm):
    title = forms.CharField(
        label='title', max_length=100, widget=forms.TextInput
        (attrs={
            'class': 'form-control',
            'placeholder': 'Unique, catchy title', 
            'required': 'required', 
            'data-custom-attr': 'custom-value'}
            )
        )
    content = forms.CharField(
        label='', widget=forms.Textarea
        (attrs={
            'class': 'form-control',
            'placeholder': 'Dont overthink it its just an idea or thought your writing about. PS; We recommend you use a laptop to write but a phone works too', 
            'required': 'required', 
            'data-custom-attr': 'custom-value'}
            )
        )
    spaces = forms.ChoiceField(
    label="spaces",
    choices=[
        ("MUSIC AND ART", "Music and Art"),
        ("CYBER-SECURITY", "Ethical Hacking"),
        ("FOOD AND LIFESTYLE", "Food and life"),
        ("LIFE HACKS AND JOBS", "Money and Jobs"),
        ("PROGRAMMING AND DATA SCIENCE", "Coding"),
        ],
    widget=forms.Select(
        attrs={'class': 'form-control',
               'data-placeholder': 'Any color',
               'data-close-on-select': 'false',
               'style': 'max-width:280px; max-height:36px;',
               'title': 'Type a word to filter the menu',}
        )
    )
    image=forms.ImageField()
    class Meta:
        model=blogpost
        fields=['title','content','spaces','image','value']
        
class RatingForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder':"write an honest comment about your interaction with the job owner and if you would recconmend them or not", 
            'required': 'required', 
            'data-custom-attr': 'custom-value'
        })
    )
    rating = forms.ChoiceField(
        choices=JobRating.StarRating.choices,
        widget=forms.Select,
        required=True,  # Ensure this is set to True
    )
    class Meta:
        model = JobRating
        fields = ['rating', 'comment'] 