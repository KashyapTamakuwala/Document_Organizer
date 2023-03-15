from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Users.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
# Create your views here.

class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self,request):
        serializer = RegisterSerializer(data=request.data,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class Login(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
    
#     def post(self,request):
#         get_user_model().objects.filter(email="")
