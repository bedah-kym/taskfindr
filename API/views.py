from rest_framework import generics,permissions
from  .serializers import BlogSerializer
from . permissions import IsStaffEditorPermissions

from blog.models import blogpost

class Bloglistview(generics.ListAPIView):
    permission_classes=[IsStaffEditorPermissions]
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer


class Blogdetailview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsStaffEditorPermissions]
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"
    user_field= "author"

class MyBlogs(generics.ListAPIView):
    #change this to a blog view that filters using username from the url then use foreignkey serialization to show blog reactions
    permission_classes=[IsStaffEditorPermissions]
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer
    user_field ="author" 
    # modify perform create function so the user is saved as default or check it in the video 4.04.39

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        data = qs.filter(author=user)
        return data
    

