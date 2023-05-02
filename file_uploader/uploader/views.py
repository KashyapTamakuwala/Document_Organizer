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
    
    # def get(self, request, pk,filename=None, format=None):

    #     # file = self.get_object(pk)
    #     # serializer = FileSerializer(file)  
    #     # data=[]
    #     # for f in file:
    #     #     serializer=FileSerializer(f)
    #     #     data.append(serializer.data)
    #     return Response(status=status.HTTP_200_OK)
    
    # define search by file name for a user


    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk,name, format=None):
        if name == None:
            return Response("Provide a valid name",status=status.HTTP_404_NOT_FOUND)
        file = self.get_object(pk,name)
        if file.exists:
            file.delete()
        else:
            return Response("Provide a valid name",status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # keep only signle file upload in real project and make it async in file management
    def post(self, request, format=None):

        
        print(request.data)

        serializer = FileSerializer(data=request.data)
        
        files_list = request.FILES.getlist('one_file')
        error=[]
        if serializer.is_valid():
            for item in files_list:
                if self.get_object(request.data['user_id'],item.name).exists():
                    error.append("File named "+item.name+" already exist")
                    #return Response("File with same name already exist",status=status.HTTP_409_CONFLICT)
                else:
                    f = File.objects.create(user_id=request.data['user_id'],name=item.name, one_file=item)
            if len(error)>0:
                return Response(error,status=status.HTTP_409_CONFLICT)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            
        
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
        file = self.get_object(pk,name)
        print(len(file))
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        print(BASE_DIR)
        if len(file) == 0:
            response = Response("Not Found",status=status.HTTP_404_NOT_FOUND)
        elif len(file) == 1:
            serializer = FileSerializer(file[0])
            filename = serializer.data['name']
            filepath = BASE_DIR + serializer.data['one_file']
            mime_type, _ = mimetypes.guess_type(filepath)
            response = HttpResponse(FileWrapper(open(filepath,'rb')), content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
        else:
            filepathlist=[]
            for f in file:
                serializer = FileSerializer(f)
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