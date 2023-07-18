from rest_framework import generics
from  .serializers import BlogSerializer,SafeBlogSerializer
from blog.models import blogpost

class Bloglistview(generics.ListAPIView):
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer


class Blogdetailview(generics.RetrieveUpdateDestroyAPIView):
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"
    user_field= "author"

class MyBlogs(generics.ListCreateAPIView):
    queryset = blogpost.objects.all()
    serializer_class = BlogSerializer
    user_field ="author" 

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        data = qs.filter(author=user)
        return data
    

