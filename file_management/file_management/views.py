from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import FolderSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FolderDetails, DataobjectForm
import traceback
import logging
from .helper import callUploaderService, getpath
import ast


# view for registering users
class FolderAPI(APIView):

    def get_data(self,pk,fol='root',cat='None'):
        try:
            if cat == 'None':
                folders = FolderDetails.objects.filter(User_id=pk,Folder_Name=fol)
                data = []
                for i in range(len(folders)):
                    ser = FolderSerializer(folders[i])
                    d = ser.data
                    d['FileList'] = ast.literal_eval(d['FileList'])
                    data.append(d)
                
                return data
            else:
                folders = FolderDetails.objects.filter(User_id=pk)
                data = []
                for i in range(len(folders)):
                    ser = FolderSerializer(folders[i])
                    d = ser.data
                    d['FileList'] = ast.literal_eval(d['FileList'])
                    for file in d['FileList'] :
                        if file['Category'] == cat:
                            data.append(file)
                return data
                
        except Exception as e:
            logging.error(traceback.format_exc())
            return Response("Not able to fetch Data",status=status.HTTP_404_NOT_FOUND)



    def get(self,request,pk,format=None):
        print("mapp here")
        fol = request.GET.get('fol','root')
        cat = request.GET.get('cat','None')
        print(fol,cat)
        data = self.get_data(pk,fol,cat)
        return Response(data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):

        obj=FolderDetails.objects.filter(Folder_Name=request.data['Parent_Folder'],
                                         User_id=request.data['User_id'])
        
        ## check if parent folder exist
        if obj.exists():
            if request.data['type']=='Folder':
                print("if folder")
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
                                            'Family':"Folder",
                                            'Category':"type1"})
                        updateparent.update(FileList=templist)

                        return Response("Folder Created",status=status.HTTP_201_CREATED)
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        return Response("Folder Creation Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            #
            elif request.data['type']=='File':
                print("if file")
                ##check if file exist
                try:
                    fol = FolderDetails.objects.filter(Folder_Name=request.data['Parent_Folder'],
                                            User_id=request.data['User_id'])
                    
                    lis = fol.get().FileList
                    for i in lis:
                        if i['Family']=='File' and i['Name']==request.data['Name']:
                            return Response("Files exist",status=status.HTTP_409_CONFLICT)
                    
                    

                    ## Call file uploader api and category define api                    
                    res = callUploaderService(request.data['Name'],request.data['User_id'],request.FILES.getlist('Files')[0])
                    path = getpath(userid=request.data['User_id'],name=request.data['Name'])

                    print(res)
                    ## upadate file list in parent folder
                    lis.append({'File_id':1,
                                'Name':request.data['Name'],
                                'Path':path,
                                'Family':"File",
                                'Category':"Book"})
                    
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
            print("object not exist")
            if request.data['Parent_Folder']!='root':
                return Response("Invalid Parent Folder",status=status.HTTP_404_NOT_FOUND)
            else:
                
                if request.data['type']=='Folder': 
                    print("object not exist if folder")
                    try:
                        ## create requested folder
                        creaetfolder = FolderDetails.objects.create(User_id=request.data['User_id'],
                                                            Folder_Name=request.data['Name'],
                                                            FileList=[]
                                                            ) 

                        ## created root folder with Update File list
                        updateparent = FolderDetails.objects.create(User_id=request.data['User_id'],
                                                            Folder_Name='root',
                                                            FileList=[{'File_id':-1,'Name':request.data['Name'],'Path':"",'Family':"Folder",'Category':"type1"}]
                                                            ) 
                        return Response("Succefull",status=status.HTTP_201_CREATED)
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        return Response("Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                elif request.data['type']=='File':
                    print("object not exist if file")
                    try:
                        
                        ## Call file uploader api and category define api
                        res = callUploaderService(request.data['Name'],request.data['User_id'],request.FILES.getlist('Files')[0])
                        #path = getpath(userid=request.data['User_id'],name=request.data['Name'])
                        path = None
                        print(res)

                        ## created root folder with Update File list
                        createfile = FolderDetails.objects.create(User_id=request.data['User_id'],
                                                            Folder_Name='root',
                                                            FileList=[{'File_id':1,
                                                                       'Name':request.data['Name'],
                                                                       'Path':path,
                                                                       'Family':"File",
                                                                       'Category':"type1"}]
                                                            ) 
                        return Response("Succefull",status=status.HTTP_201_CREATED)
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        return Response("Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response("Invalid Type",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    
class FolderCatAPI(APIView):
    def get(self,request,pk,cat='None',format=None):
        print("mapp here 2")
        try:
            folders = FolderDetails.objects.filter(User_id=pk)
            data=[]
            for i in range(len(folders)):
                ser = FolderSerializer(folders[i])
                d = ser.data
                da = ast.literal_eval(d['FileList'])
                for file in da:
                    if file['Category'] == cat:
                        data.append(file)
        except Exception as e:
            logging.error(traceback.format_exc())
            return Response("Not able to fetch Data",status=status.HTTP_404_NOT_FOUND)
        return Response(data,status=status.HTTP_200_OK)
