from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FileSerializer
from .models import File
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import zipfile
import mimetypes
import os
from pathlib import Path
from wsgiref.util import FileWrapper
import requests
import urllib.request
import urllib.parse
from .ml_classification import getCategory

   


class Files_APIView_Detail(APIView):
    #parser_class = (FileUploadParser, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    #permission_classes = (permissions.AllowAny,)

    def get_object(self, pk,name=None): 
        if name==None:
            try:
                return File.objects.all().filter(user_id=pk)
            except File.DoesNotExist:
                raise Http404
        else:
            try:
                return File.objects.all().filter(user_id=pk,name=name)
            except  File.DoesNotExist:
                raise Http404
    
    # search by userid    
    def get(self, request, pk,name=None, format=None):
        ## check name and determine path.

        file = self.get_object(pk,name)
        # serializer = FileSerializer(file)  
        data=[]
        if len(file)==0:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)
        for f in file:
            serializer=FileSerializer(f)
            data.append(serializer.data)
        return Response(data,status=status.HTTP_200_OK)
    



    # keep only signle file upload in real project and make it async in file management
    def post(self, request, format=None):

        
        #print(request.data)

        serializer = FileSerializer(data=request.data)
        
        files_list = request.FILES.getlist('one_file')
        error=[]
        re = []
        if serializer.is_valid():
            for item in files_list:
                if self.get_object(request.data['user_id'],item.name).exists():
                    error.append("File named "+item.name+" already exist")
                    #return Response("File with same name already exist",status=status.HTTP_409_CONFLICT)
                else:
                    f = File.objects.create(user_id=request.data['user_id'],name=item.name, one_file=item)
                    fi = self.get_object(request.data['user_id'],item.name).first()
                    serializer=FileSerializer(fi)
                    data = serializer.data
                    data['category'] = getCategory(data['one_file'])

                    # print("fi",serializer.data)
                    re.append(data)
            if len(error)>0:
                return Response(error,status=status.HTTP_409_CONFLICT)
            else:
                return Response(re, status=status.HTTP_201_CREATED)

            
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class File_Download_Api(APIView):

    def get_object(self, pk,name=None): 
        if name==None:
            try:
                return File.objects.all().filter(user_id=pk)
            except File.DoesNotExist:
                raise Http404
        else:
            try:
                return File.objects.all().filter(user_id=pk,name=name)
            except  File.DoesNotExist:
                raise Http404

    
    # search by userid    
    def get(self, request, pk,name=None, format=None):
        ## check name and determine path.
        name = request.GET.get('name').split(",")
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        print(BASE_DIR)
        if len(name) == 0:
            response = Response("Not Found",status=status.HTTP_404_NOT_FOUND)
        elif len(name) == 1:
            file = self.get_object(pk,name[0])
            serializer = FileSerializer(file[0])
            filename = serializer.data['name']
            filepath = BASE_DIR + serializer.data['one_file']
            mime_type, _ = mimetypes.guess_type(filepath)
            response = HttpResponse(FileWrapper(open(filepath,'rb')), content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
        else:
            filepathlist=[]
            for n in name:
                file = self.get_object(pk,n)
                serializer = FileSerializer(file[0])
                filepath = BASE_DIR + serializer.data['one_file']
                filepathlist.append(filepath)
            zipdestinationpath = BASE_DIR + '/media/document/{id:d}/out.zip'
            zipdestinationpath=zipdestinationpath.format(id=pk)
            with zipfile.ZipFile(zipdestinationpath,'w') as zipMe:
                for file in filepathlist:
                    zipMe.write(file,compress_type=zipfile.ZIP_DEFLATED)
            zipMe.close()
            mime_type, _ = mimetypes.guess_type(zipdestinationpath)
           
            response = HttpResponse(FileWrapper(open(zipdestinationpath,'rb')), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="{filename}.zip"'.format(
                filename = "Out"
            )
            file_path = Path(zipdestinationpath)
            file_path.unlink()

        return response
    

class File_Stream_Api(APIView):

    def get_object(self, pk,name=None): 
        if name==None:
            try:
                return File.objects.all().filter(user_id=pk)
            except File.DoesNotExist:
                raise Http404
        else:
            try:
                return File.objects.all().filter(user_id=pk,name=name)
            except  File.DoesNotExist:
                raise Http404

    
    # search by userid    
    def get(self, request, pk, format=None):
        ## check name and determine path.
        name = request.GET.get('name')
        file = self.get_object(pk,name)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        serializer = FileSerializer(file[0])
        filename = serializer.data['name']
        filepath = BASE_DIR + serializer.data['one_file']
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(FileWrapper(open(filepath,'rb')), content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
       

        return response
    
def delete(request, pk,name, format=None):
    print("In delete")
    if name == None:
        return Response("Provide a valid name",status=status.HTTP_404_NOT_FOUND)
    file = File.objects.all().filter(user_id=pk,name=name)
    print(file)
    if file.exists:
        file.delete()
    else:
        return HttpResponse("Provide a valid name",status=status.HTTP_404_NOT_FOUND)
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)