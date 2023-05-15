from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import FolderSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FolderDetails, DataobjectForm
import traceback
import logging
from .helper import callUploaderService
import ast
import json
from django.http.response import HttpResponse
import requests

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
                            file['Parent_Folder'] = d['Folder_Name']
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

        print("Folder",request.data)
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
                    up_fi = []
                    for fi in request.FILES.getlist('Files'):                
                        res = callUploaderService(request.FILES.getlist('Files')[0].name,request.data['User_id'],fi)
                        up_fi.append(res.text)

                    print(up_fi)
                    for iter in up_fi:
                        d = ast.literal_eval(iter)
                        print("heree",d)
                        ## upadate file list in parent folder
                        lis.append({'File_id':1,
                                    'Name':d[0]['name'],
                                    'Path':d[0]['one_file'],
                                    'Family':"File",
                                    'Category':d[0]['category']})
                    
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
                        up_fi = []
                        for f in request.FILES.getlist('Files'):
                            res = callUploaderService(request.FILES.getlist('Files')[0].name,request.data['User_id'],f)
                            up_fi.append(res.text)
                        
                        print("up_fi",up_fi)
                        temp =[]
                        for iter in up_fi:
                            d = ast.literal_eval(iter)
                            temp.append({'File_id':1,
                                        'Name':d[0]['name'],
                                        'Path':d[0]['one_file'],
                                        'Family':"File",
                                        'Category':d[0]['category']})

                        ## created root folder with Update File list
                        createfile = FolderDetails.objects.create(User_id=request.data['User_id'],
                                                            Folder_Name='root',
                                                            FileList=temp
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


class FolderDelete(APIView):

    # def getfile(self,folder_name_lis,li=[]):
    #     pass

    def getFolder(self,pk,folder_list=[],file_list=[]):
        fol_list = [folder_list[0]]
        while len(folder_list) !=0 :
            folder_name = folder_list[0]
            f = FolderDetails.objects.filter(User_id=pk,Folder_Name=folder_name)
            getfolder = f.get()
            ser = FolderSerializer(getfolder)
            d = ser.data
            d['FileList'] = ast.literal_eval(d['FileList'])
            for i in d['FileList']:
                if i['Family'] == 'File':
                    file_list.append(i['Name'])
                else:
                    folder_list.append(i['Name'])
                    fol_list.append(i['Name'])
            folder_list.pop(0)
        return file_list,fol_list

    def post(self,request,pk):
        Parent_folder = request.data['name']
        file_name = request.data['fname']

        try:
            folders = FolderDetails.objects.filter(User_id=pk,Folder_Name=Parent_folder)
            getfolder = folders.get()
            ser = FolderSerializer(getfolder)
            d = ser.data
            d['FileList'] = ast.literal_eval(d['FileList'])
            temp=[]
            for i in d['FileList']:
                if i['Name'] == file_name:
                    if i['Family']=='File':
                        url = "http://fileuploader:7003/file/delete/{userid}/{name}".format(userid=pk,name=file_name)
                        print(url)
                        response = requests.get(url)
                        continue
                    else:
                        file_list,folder_list = self.getFolder(pk,folder_list = [i['Name']])
                        for f in file_list:
                            url = "http://fileuploader:7003/file/delete/{userid}/{name}".format(userid=pk,name=f)
                            print(url)
                            response = requests.get(url)
                        for j in folder_list:
                            f = FolderDetails.objects.filter(User_id=pk,Folder_Name=j)
                            f.update(FileList=[])
                        continue

                else:
                    temp.append(i)
            
            folders.update(FileList=temp)
        except Exception as e:
            print(e)
            return HttpResponse("Error",status=status.HTTP_204_NO_CONTENT)
        return HttpResponse("Delete",status=status.HTTP_204_NO_CONTENT)
    