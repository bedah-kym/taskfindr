from blog.models import blogpost
from rest_framework import serializers
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    blog = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    class Meta:  
        model=blogpost
        fields = [
            'title','spaces','date_posted','author','blog'
        ]

    def get_blog(self,obj):
        return(
            f"http://127.0.0.1:8100/post/{obj.pk}/"
        )
    def get_author(self,obj):
         username=obj.author.username
         return username
    
class SafeBlogSerializer(serializers.ModelSerializer):
    blog = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = blogpost
        fields = ['title','spaces','blog','content']

    def get_blog(self,obj):
        return(
            f"http://127.0.0.1:8100/post/{obj.pk}/"
        )