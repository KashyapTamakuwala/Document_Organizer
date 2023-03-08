from django.urls import path
from .views import *

app_name = 'file_uploader'

urlpatterns = [
    # File 
    path('file/', Files_APIView_Detail.as_view()), 
    path('file/<int:pk>/', Files_APIView_Detail.as_view()),
    path('file/<int:pk>/<str:name>/', Files_APIView_Detail.as_view()),
    
]