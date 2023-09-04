from django.shortcuts import get_object_or_404
from rest_framework import generics,permissions
from  .serializers import BlogSerializer,postreactionserializer
from . permissions import IsStaffEditorPermissions
from blog.models import blogpost,Postreaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from google_auth_oauthlib.flow import Flow

""" this api is built for mainly data analysis so we can use it to monitor who likes what
and also push posts based on popularity.it can be expanded to see who does most tasks or
who is inactive so they get an email or smth.
"""

    
class Bloglistview(generics.ListAPIView):
    permission_classes=[IsStaffEditorPermissions]
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer


class Blogdetailview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsStaffEditorPermissions]
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"
  

class MyBlogs(generics.ListAPIView):
    #change this to a blog view that filters using username from the url then use foreignkey serialization to show blog reactions
    permission_classes=[IsStaffEditorPermissions]
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer
    # modify perform create function so the user is saved as default or check it in the video 4.04.39

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        data = qs.filter(author=user)
        return data
    
class Postreactionview(generics.ListAPIView):
    """ this view will get you all the reactions on 
    a particular post 
    """
    permission_classes=[IsStaffEditorPermissions]
    queryset = Postreaction.objects.all()
    serializer_class = postreactionserializer

    def get_queryset(self):
        qs = super().get_queryset()
        pk = self.kwargs.get('pk')
        blog = get_object_or_404(blogpost,id=pk)
        data = qs.filter(post=blog)
        return data

def youtube_oauth_callback(request):
    flow = Flow.from_client_secrets_file(
        'path/to/client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube.readonly'],
        redirect_uri=request.build_absolute_uri(reverse('youtube_oauth_callback'))
    )

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    print(credentials)
    # Store 'credentials' in your database associated with the user

    return HttpResponseRedirect(reverse('profile'))
