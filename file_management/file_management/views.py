from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import FolderSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FolderDetails
import traceback
import logging


# view for registering users
class FolderAPI(APIView):
    def get(self,request,pk,fol='root',format=None):
        print("mapp here")
        try:
            folders = FolderDetails.objects.filter(User_id=pk,Folder_Name=fol)
            data=[]
            for i in range(len(folders)):
                ser = FolderSerializer(folders[i])
                data.append(ser.data)
        except Exception as e:
            logging.error(traceback.format_exc())
            return Response("Not able to fetch Data",status=status.HTTP_404_NOT_FOUND)
        return Response(data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):

        ## first check if pk and folder exist or not
        obj = FolderDetails.objects.filter(User_id=request.data['User_id'],Folder_Name=request.data['Name'])
        if obj.exists():
            if request.data['type']=='Folder':
                return Response("Folder with Same Name exist",status=status.HTTP_302_FOUND)
            else:
                f = obj.get()
                ##call upload file api
                f.FileList = [{'File_id':1,'Name':request.data['Name'],'Path':'','Family':'Fi','Category':'type1'}]
                f.save() 
        else:
            ## Creating a new folder 
            try:
                parent_object=FolderDetails.objects.filter(User_id=request.data['User_id'],Folder_Name=request.data['Parent_Folder'])
                if parent_object.exists():
                    print("in if")
                    # folder = FolderDetails()
                    # folder.User_id = request.data['User_id'] 
                    # folder.Folder_Name = request.data['Name']
                    # folder.FileList = [] 
                    # folder.save()
                    print("updating parent")
                    ## find a way to update array list of parent folder
                    print(parent_object.get())
                    # temp = parent_object.update(FileList.append())
                    return Response("Folder "+request.data['Name']+" Created",status=status.HTTP_201_CREATED)
                else:
                    if request.data['Name']=='root':
                        folder = FolderDetails()
                        folder.User_id = request.data['User_id'] 
                        folder.Folder_Name = request.data['Name']
                        folder.FileList = [] 
                        folder.save()
                        return Response("Root Folder Created",status=status.HTTP_201_CREATED)
                    else:
                        return Response("Parent Folder Do not exist",status=status.HTTP_404_NOT_FOUND) 
            except Exception as e:
                logging.error(traceback.format_exc())
                return Response("error",status=status.HTTP_425_TOO_EARLY)

        # if request.data['type']=='Folder':
        #     try:
        #         folder = FolderDetails()
        #         folder.User_id = request.data['User_id'] 
        #         folder.Folder_Name = request.data['Current_Folder']
        #         folder.FileList = [{'File_id':-1,'Name':request.data['Name'],'Path':'','Family':'Fo','Category':'type1'}] 
        #         folder.save()
        #     except Exception as e:
        #         logging.error(traceback.format_exc())
        #         return Response("error",status=status.HTTP_425_TOO_EARLY)

        # else:
        #     Response("in else",status=status.HTTP_100_CONTINUE)

        return Response(folder.User_id,status=status.HTTP_201_CREATED)
    

