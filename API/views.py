from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from .serializers import BlogSerializer,postreactionserializer
from . permissions import IsStaffEditorPermissions
from blog.models import blogpost,Postreaction
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.core.cache import cache
import os
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

def get_youtube_service():
    API_KEY =os.environ.get('YOUTUBE_API_KEY')
    """Builds the YouTube service object."""
    return build('youtube', 'v3', developerKey=API_KEY)

def get_comments(service, video_id):
    """Fetches comments from a YouTube video."""
    try:
        
        request = service.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText'
        )
        response = request.execute()
        
        comments = response.get('items', [])
        while 'nextPageToken' in response:
            response = service.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                pageToken=response['nextPageToken']
            ).execute()
            comments.extend(response.get('items', []))
        return comments
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')

VIDEO_ID = "e9OcytXzBsU"
def verify_comment(request):
    service = get_youtube_service()
    cache_key = f'comments_{VIDEO_ID}'
    comments = cache.get(cache_key)
    
    if not comments:
        # If not in cache, fetch from YouTube API and cache the results
        comments = get_comments(service, VIDEO_ID)
        cache.set(cache_key, comments, timeout=60*10)  # Cache for 10 minutes
    for comment in comments:  
            author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
            if author == '@user-ss1pj7ej4y':
                found=True
                break
            found=False
                
    return render(request, 'blog/comments.html', {'match': found})