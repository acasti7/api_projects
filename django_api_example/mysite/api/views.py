from django.shortcuts import render
from rest_framework import generics, status
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

## generics allow you to update/delete models as needed...
# Create your views here.
# ORM: "object relational mapping"

#The below generic API view allows users to create new blog posts, and get new blogposts that already exist...
class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all() # gets all instances of model.
    serializer_class = BlogPostSerializer

    def delete(self, request, *args, **kwargs):
        '''
        this deletes all blog posts...
        '''
        BlogPost.objects.all().delete() # refers to the model class
        return Response(status=status.HTTP_204_NO_CONTENT) #this is what should be returned when deleting something...


class BlogPostRetrieverUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all() # gets all instances of model.
    serializer_class = BlogPostSerializer
    lookup_field = "pk" ## primary key of the blogpost....

### custom views for API.... ###
class BlogPostList(APIView):
    '''
    simple api view which allow user to query based on the name of an object
    '''
    def get(self, request, format = None):
        title = request.query_params.get("title","") #get all titles...
        print("Title received:", title)  # Debugging output
        
        if title:
            #filter the blog posts based on the title...
            blog_posts = BlogPost.objects.filter(title__icontains=title)
            print("Filtered Queryset:", blog_posts.query)  # See the actual SQL query

        else:
            #if no title is provided, return all blog posts
            blog_posts = BlogPost.objects.all()
            print("Unfiltered Queryset (All posts):", blog_posts.query)  # Debugging output

    
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)