##"json": javascript object notation
## Serializers takes instances of python objects (e.g. models) and converts it into something that can be interacted with from the API
from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id","title","content","published_date"] ## note this has to be specified for the API to interact with those fields in the data model...
        