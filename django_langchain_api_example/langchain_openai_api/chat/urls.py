from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('chat/',views.chat),
    path('chat/delete/',views.delete_conversation),
    path('chat/get-titles',views.get_title),
    path('chat/get-data/', views.get_data)
]

'''
Don’t forget to add an Authentication header with every request written below having value: “Token your_auth_token” This auth token is got from localhost:8000/get-auth.

If you want to create a new conversation create a POST request with JSON body having parameters {“prompt”: “your question to the model” } on localhost:8000/chat/
To continue the last conversation add a title to request parameters {“title”: “conversation_title”, “prompt”: “your question to the model” } on the above request
To get all titles of conversations create a GET request on localhost:8000/chat/get-titles
To delete a conversation, create a POST request on localhost:8000/chat/delete/
'''