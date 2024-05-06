from django.urls import path
from . import views

# the view is the root and what is rendered onto screen
# url is how we get there...

urlpatterns = [
    path("blogposts/", views.BlogPostListCreate.as_view(),name = "blogpost-view-create"),
    path("blogposts/<int:pk>/", views.BlogPostRetrieverUpdateDestroy.as_view(), name="update"),
    path("blogposts/search/", views.BlogPostList.as_view(), name="blogpost-list")
] 
#the url "blogposts/", is how we get to this view
#the url "blogposts/<int:pk>/" will allow us to remove or update or retrieve value... when accessing using this url
#the url "blogposts/search/?title=your-search-title-here" will allow a search across posts based on the title
