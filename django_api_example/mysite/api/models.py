from django.db import models

# Create your models here.
class BlogPost(models.Model):
    '''
    Inherits the base data model 
    --need to define the fields/columns in the model
    --think of this as a table in a SQL database
    --the below are the fields, and the relevant datatypes
    '''
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
