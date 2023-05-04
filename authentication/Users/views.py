from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Users.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
# Create your views here.

class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self,request):
        try: 
            serializer = RegisterSerializer(data=request.data,many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response("Invalid",status=status.HTTP_400_BAD_REQUEST)

class Userid(APIView):
    def post(self,request):
        # print("Userid_get")
        try:
            token = request.data['token']
            uid = AccessToken(token)['user_id']
            return Response(uid,status=status.HTTP_200_OK)
        except:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

# class Login(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
    
#     def post(self,request):
#         get_user_model().objects.filter(email="")
