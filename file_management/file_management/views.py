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

        obj=FolderDetails.objects.filter(Folder_Name=request.data['Parent_Folder'],
                                         User_id=request.data['User_id'])
        
        ## check if parent folder exist
        if obj.exists():
            if request.data['type']=='Folder':

                ## check if folder with same name exist
                ## bug free if
                if FolderDetails.objects.filter(Folder_Name=request.data['Name'],
                                         User_id=request.data['User_id']).exists():
                    return Response("Folder exist",status=status.HTTP_409_CONFLICT)
                
                 
                else:
                    try:
                        ## create folder
                        creaetfolder = FolderDetails.objects.create(User_id=request.data['User_id'],
                                                                    Folder_Name=request.data['Name'],
                                                                    FileList=[]
                                                                    )
                        
                        updateparent = FolderDetails.objects.filter(Folder_Name=request.data['Parent_Folder'],
                                                            User_id=request.data['User_id']
                                                            )
                        templist = updateparent.get().FileList
                        templist.append({'File_id':-1,
                                            'Name':request.data['Name'],
                                            'Path':"",
                                            'Family':"Fo",
                                            'Category':"type1"})
                        updateparent.update(FileList=templist)

                        return Response("Folder Created",status=status.HTTP_201_CREATED)
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        return Response("Folder Creation Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            #
            elif request.data['type']=='File':

                ##check if file exist
                try:
                    fol = FolderDetails.objects.filter(Folder_Name=request.data['Parent_Folder'],
                                            User_id=request.data['User_id'])
                    
                    lis = fol.get().FileList
                    for i in lis:
                        if i['Family']=='Fi' and i['Name']==request.data['Name']:
                            return Response("Files exist",status=status.HTTP_409_CONFLICT)
                    
                    

                    ## Call file uploader api and category define api

                    ## upadate file list in parent folder
                    # contains bugs
                    lis.append({'File_id':1,
                                'Name':request.data['Name'],
                                'Path':"",
                                'Family':"Fi",
                                'Category':"type1"})
                    
                    fol.update(FileList=lis)
                    return Response("File Created",status=status.HTTP_201_CREATED)
                
                except Exception as e:
                    logging.error(traceback.format_exc())
                    return Response("File Creation Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            ## no bug 
            else:
                return Response("Invalid Type",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        ## bug free
        else:
            ## parent folder and pk do not exit() then check if parent folder is root or not

            if request.data['Parent_Folder']!='root':
                return Response("Invalid Parent Folder",status=status.HTTP_404_NOT_FOUND)
            else:
                
                if request.data['type']=='Folder': 
                    
                    try:
                        ## create requested folder
                        creaetfolder = FolderDetails.objects.create(User_id=request.data['User_id'],
                                                            Folder_Name=request.data['Name'],
                                                            FileList=[]
                                                            ) 

                        ## created root folder with Update File list
                        updateparent = FolderDetails.objects.create(User_id=request.data['User_id'],
                                                            Folder_Name='root',
                                                            FileList=[{'File_id':-1,'Name':request.data['Name'],'Path':"",'Family':"Fo",'Category':"type1"}]
                                                            ) 
                        return Response("Succefull",status=status.HTTP_201_CREATED)
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        return Response("Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                elif request.data['type']=='File':
                    try:
                        
                        ## Call file uploader api and category define api


                        ## created root folder with Update File list
                        createfile = FolderDetails.objects.create(User_id=request.data['User_id'],
                                                            Folder_Name='root',
                                                            FileList=[{'File_id':1,'Name':request.data['Name'],'Path':"",'Family':"Fi",'Category':"type1"}]
                                                            ) 
                        return Response("Succefull",status=status.HTTP_201_CREATED)
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        return Response("Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response("Invalid Type",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

