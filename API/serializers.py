from blog.models import blogpost,Postreaction
from rest_framework import serializers
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    blog = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    class Meta:  
        model=blogpost
        fields = [
            'title','spaces','date_posted','author','blog','likes','dislikes'
        ]

    def get_blog(self,obj):
        return(
            f"http://127.0.0.1:8100/post/{obj.pk}/"
        )
    def get_author(self,obj):
         username=obj.author.username
         return username
    
    def get_likes(self,obj):
        likes = Postreaction.objects.filter(post=obj,reaction="like")
        likes = likes.count()
        print (likes)
        return likes
    
    def get_dislikes(self,obj):
        dislikes = Postreaction.objects.filter(post=obj,reaction="dislike")
        dislikes = dislikes.count()
        return dislikes
    
class SafeBlogSerializer(serializers.ModelSerializer):
    blog = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = blogpost
        fields = ['title','spaces','blog','content']

    def get_blog(self,obj):
        return(
            f"http://127.0.0.1:8100/post/{obj.pk}/"
        )
    
class postreactionserializer(serializers.ModelSerializer):
    fan = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Postreaction
        fields = [
            'fan','post','reaction'
        ]
    
    def get_fan(self,obj):
         username=obj.fan.username
         return username
    
    