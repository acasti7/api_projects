from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

 
## This decorator is used to exempt the view from the CSRF (Cross-Site Request Forgery)
# protection provided by Django's CSRF middleware. It allows the view to accept requests without requiring a CSRF token.
@csrf_exempt
def auth(request, format = None):
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse("Added Successfully!!", safe=False)
    return JsonResponse("Invalid Format", safe=False)
