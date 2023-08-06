# -*- coding: latin-1 -*-

import sys,os
import time
import bz2
import hashlib
import json
import requests
import numpy as np
from http.client import HTTPConnection
from urllib.parse import urlencode

from morphonet.tools import addslashes,tryParseInt,strblue,strred,strgreen,nodata,ss

class Net:

    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    def __init__(self,login,passwd,new_url=None,new_port=-1): 
        self.id_people=-1
        self.id_dataset=-1
        self.token = ""
        self.id_dataset_owner=-1
        self.minTime=-1
        self.maxTime=-1
        self.login=login
        self.passwd=passwd
        self.bundle=0
        self.id_NCBI=1 #0 -> Unclassified 
        self.id_type=0; #0 Observed Data, 1 Simulated Data, 2 Drawing Data
        self.guys={}
        self.datasettype={}
        if new_url is not None:
             self.url=new_url
        else:
            from morphonet import url
            self.url=url
        if new_port!=-1:    
            self.port=new_port 
        else:
            from morphonet import port
            self.port=port
        self._connect()

    def _getHeaders(self):
        if self.token == "":
            return {"Content-Type": "application/json"}
        return {"Content-Type": "application/json",'Authorization':'Token '+self.token}

    def _connect(self):
        #HTTPConnection.debuglevel = 1
        conn = HTTPConnection(self.url)
        params = json.dumps({'username': self.login, 'password': self.passwd})
        conn.request("POST", "/rest-auth/login/",params,self._getHeaders())
        response=conn.getresponse()
        if response.status==200:
            data=json.loads(str(response.read().decode("utf-8")))
            conn.close()
            self.id_people=data['user']
            self.token=data['key']
            print(strblue(self.login+' is connected to MorphoNet'))
            return True
        else:
            print(strred('CONNECTION ERROR '+str(response.status)+" "+response.reason))
        conn.close()
        return False
        
    def _isConnected(self):
        if self.id_people==-1:
            print(strred(' ERROR : You are not connected '))
            return False
        return True
    def _request(self,param,path,request_type):
        if self._isConnected():
            conn = HTTPConnection(self.url,timeout=100)
            try:
                conn.request(request_type, path,json.dumps(param), self._getHeaders())
                response=conn.getresponse()
                if response.status==200:
                    da=json.loads(str(response.read().decode("utf-8")))
                    conn.close()
                    return da
                else:
                    print(strred('CONNECTION ERROR '+str(response.status)+" "+response.reason))
                    quit()
            except  Exception as e:
                print('Error cannot request ... '+str(e))
                time.sleep(5)
                print(' --> Retry')
                return self._request(param,path,request_type)
            conn.close()   
    def binary_request(self,param,path,request_type):
        if self._isConnected():
            conn = HTTPConnection(self.url,timeout=100)
            try:
                conn.request(request_type, path,json.dumps(param), self._getHeaders())
                response=conn.getresponse()
                if response.status==200:
                    da=response.read()
                    conn.close()
                    return da
                else:
                    print(strred('CONNECTION ERROR '+str(response.status)+" "+response.reason))
                    quit()
            except  Exception as e:
                print('Error cannot request ... '+str(e))
                time.sleep(5)
                print(' --> Retry')
                return self._request(param,path,request_type)
            conn.close()   
    def _large_request(self,param,path,data):
        if self._isConnected():
            try:
                if os.path.isfile("temp.bz2"):
                    os.system('rm -f temp.bz2')
                if sys.version_info[0]>=3: #PYTHON 3
                    if isinstance(data,str):
                        data=bytes(data.encode('utf-8'))
                    with bz2.open("temp.bz2", "wb") as f:
                        unused = f.write(data)
                files = {'file': open("temp.bz2", 'rb')}
                session = requests.Session()
                del session.headers['User-Agent']
                del session.headers['Accept-Encoding']
                session.headers['Authorization'] = 'Token '+self.token 
                r = session.post("http://"+self.url+path, files=files,data=param)
                if r.status_code == requests.codes.ok:
                    return r.text
                else:
                    print(strred('CONNECTION ERROR '+str(r.status_code)))
                    quit()
                if os.path.isfile("temp.bz2"):
                    os.system('rm -f temp.bz2')
            except  Exception as e:
                print('ERROR cannot request ... '+str(e))
                quit()
     
    
    #LOOK FOR SOMEONE IN THE DATABASE
    def getGuys(self): 
        data=self._request({},'/api/people/','GET')
        for g in data:
            self.guys[int(g['id'])]=g['surname']+" "+g['name']
    def getGuyByID(self,id_guy): # RETURN NAME + SURNAME + LOGIN FORM SPECIFIC ID
        id_guy=int(id_guy)
        if self.guys=={}:
            self.getGuys()
        if id_guy in self.guys:
            return self.guys[id_guy]
        data=self._request({},'/api/people/'+str(id_guy),'GET')
        if data=="[]":
            return strred("unkown")
        else:
            return data
    def getGuyByName(self,name): # RETURN NAME + SURNAME + LOGIN FORM SPECIFIC ID
        values = name.split(' ')
        u_name = str(values[0])
        u_surname = str(values[1])
        data=self._request({'name':u_name,'surname':u_surname},'/api/userbyname/','GET')
        if nodata(data):
            print(strred('User is unknown or input is incorrect. Please input as "name surname"'))
            quit()
        if data=="[]":
            print(strblue(ss+str(name)+" is unkown"))
            return -1
        else:
            #dataset=json.loads(data)
            return int(data['id'])
    def getGroupByName(self,name): # RETURN NAME + SURNAME + LOGIN FORM SPECIFIC ID
        data=self._request({'name':name},'/api/groupidbyname/','GET')
        if nodata(data):
            print(strred('Please input as "name"'))
            quit()
        if data=="[]" or data['status'] is not None:
            print(strblue(ss+str(name)+" is unkown"))
            return -1
        else:
            #dataset=json.loads(data)
            return int(data['id'])
    #NCBI Taxonomy
    def _getNCBITypeByID(self,id_NCBI):
        if self._isConnected():
            data=self._request({},'/api/ncbitree/'+str(id_NCBI)+'/','GET')
            return data['name']
    #TYPE 
    def _getTypeName(self,id_type): #0 Observed Data, 1 Simulated Data, 2 Drawing Data
        if id_type==0:
            return "Observed Data"
        if id_type==1:
            return "Simulated Data"
        if id_type==2:
            return "Drawing Data"
        return "Unknown Data"


    #DATASET 
    def _isDataSet(self):
        if not self._isConnected():
            return False
        if self.id_dataset==-1:
            print(strgreen(ss+'you first have to select a dataset'))
            return False
        return True
    def _ownDataSet(self):
        if not self._isDataSet():
            return False
        if str(self.id_dataset_owner)!=str(self.id_people):
            print(strgreen(ss+'you are not the owner of this dataset, ask '+self.getGuyByID(self.id_dataset_owner)))
            return False
        return True  
    def _initTimePoint(self,minTime,maxTime): #INTERNAL FUNCTION TO INITIALISE TIME POINT
        self.minTime=int(minTime)
        self.maxTime=int(maxTime)
    def _parseDataSet(self,data): #Parse id,name,minTime,maxTime,id_people to dataset structure
        if nodata(data):
            print(strred(ss+'dataset not found'))
        else:
            dataset=data
            ids,ok=tryParseInt(dataset['id'])
            if not ok: 
                print(strgreen(ss+'dataset not found '+str(data)))
            else: 
                name=dataset['name']
                self._initTimePoint(dataset['mintime'],dataset['maxtime'])
                self.id_dataset_owner=dataset['id_people']
                self.bundle,ok=tryParseInt(dataset['bundle'])
                self.id_NCBI,ok=tryParseInt(dataset['id_ncbi'])
                self.id_type,ok=tryParseInt(dataset['type'])
                self.id_dataset=ids
                print(ss+'found dataset '+name+' with id ' + str(self.id_dataset)+' from '+str(self.minTime)+' to ' +str(self.maxTime)+' owned by '+str(self.id_dataset_owner)+' with type='+str(self.id_NCBI))
    def _showDataSets(self,data):
        #dataset=json.loads(data)
        for datas in data:  #id,name,minTime,maxTime,id_people,bundle,id_NCBI,type,date
            s='('+str(datas['id'])+') '+datas['name']
            if int(datas['mintime'])!=int(datas['maxtime']):
                s+=' from '+str(datas['mintime'])+' to '+str(datas['mintime'])
            s+=' is '+self._getTypeName(int(datas['type']))
            if datas['id_ncbi'] != 0 and datas['id_ncbi'] != -1:
                s+=' of '+self._getNCBITypeByID(datas['id_ncbi'])
            s+=' created by '+self.getGuyByID(datas['id_people'])
            s+=' the '+datas['date']
            print(s)
    def listMyDataSet(self): #LIST ALL MY DATASET 
        if self._isConnected():
            data=self._request({},'/api/mydataset/','GET')
            self._showDataSets(data)
    def listDataSet(self): #LIST ALL  DATASET 
        if self._isConnected():
            data=self._request({},'/api/userrelatedset/','GET')
            self._showDataSets(data)
    def shareDatasetWithUser(self,id_user,how): #SHARE A DATASET with USER
        if self._ownDataSet():
            data=self._request({"sharedataset":self.id_dataset,"id_user":id_user,"how":how},'/api/shareuserapi/','POST')
            ids,ok=tryParseInt(data['id'])
            if not ok: 
                print(strred(' ERROR : Share not created '+str(data['id'])))
            else :
                print(ss+"your share is created (with id "+str(data['id'])+')')
    def unshareDatasetWithUser(self,id_user,how): #UNSHARE A DATASET with USER
        if self._ownDataSet():
            data=self._request({"sharedataset":self.id_dataset,"id_user":id_user,"how":how},'/api/unshareuserapi/','POST')
            if data['status'] == "failed": 
                print(strred(' ERROR : Share not deleted'))
            else :
                print(ss+"your share is deleted")
    def unshareDatasetWithGroup(self,id_group,how): #SHARE A DATASET with GROUP
        if self._ownDataSet():
            data=self._request({"sharedataset":self.id_dataset,"id_group":id_group,"how":how},'/api/unsharegroupapi/','POST')
            if data['status'] == "failed": 
                print(strred(' ERROR : Share not deleted'))
            else :
                print(ss+"your share is deleted")
    def shareDatasetWithGroup(self,id_group,how): #SHARE A DATASET with GROUP
        if self._ownDataSet():
            data=self._request({"sharedataset":self.id_dataset,"id_group":id_group,"how":how},'/api/sharegroupapi/','POST')
            ids,ok=tryParseInt(data['id'])
            if not ok: 
                print(strred(' ERROR : Share not created '+str(data['id'])))
            else :
                print(ss+"your share is created (with id "+str(data['id'])+')')
    def createDataSet(self,dataname,minTime=0,maxTime=0,id_NCBI=0,id_type=0,spf=-1,dt=-1): #CREATE A NEW DATA SET
        self.id_NCBI=id_NCBI
        self.id_type=id_type
        if self._isConnected():
            data=self._request({"createdataset":dataname,"minTime":minTime,"maxTime":maxTime,"id_NCBI":self.id_NCBI,"id_type":self.id_type,"spf":spf,"dt":dt},'/api/createdatasetapi/','POST')
            self.id_dataset_owner=self.id_people
            ids,ok=tryParseInt(data)
            if not ok: 
                print(strred(' ERROR : Dataset not created '+str(data)))
            else :
                self.id_dataset=ids
                self.id_dataset_owner=self.id_people
                self._initTimePoint(minTime,maxTime)
                print(ss+"your id dataset '"+dataname+"' is created (with id "+str(self.id_dataset)+')')
    def uploadDescription(self,description): #Upload a description 
        if self._ownDataSet():
            data=self._request({"uploadescription":self.id_dataset,"description":description},'/api/uploadcommentapi/','POST')
            print(data['status'])        
    def updateDataSet(self,dataname="",minTime=-1,maxTime=-1,id_NCBI=-1,id_type=-1): #COMPLETE DELETE OF A DATASET
        if dataname!="":
            self.dataname=dataname
        if minTime!=-1:
            self.minTime=minTime
        if maxTime!=-1:
            self.maxTime=maxTime
        if id_NCBI!=-1:
            self.id_NCBI=id_NCBI 
        if id_type!=-1:
            self.id_type=id_type 
        if self._ownDataSet():
            data=self._request({"updatedataset":self.id_dataset,"minTime":self.minTime,"maxTime":self.maxTime,"id_NCBI":self.id_NCBI,"id_type":self.id_type,"dataname":self.dataname},'/api/updatesetapi/','POST')
            if nodata(data): 
                self._initTimePoint(self.minTime,self.maxTime)
            else:
                print(strred(' ERROR : '+str(data)))
    def selectDataSetById(self,ids): #SELECT A DATASET BY ID
        if self._isConnected():
            self.id_dataset=-1
            data=self._request({"dataset":ids},'/api/sitedataset/'+str(ids)+'/','GET')
            if data is not None :
                self._parseDataSet(data)
            else :
                print("No dataset found")         
    def selectDataSetByName(self,name): #SELECT A DATASET BY NAME
        if self._isConnected():
            self.id_dataset=-1
            data=self._request({"datasetname":name},'/api/datasetnameapi/','GET')
            if len(data) > 0:
                self._parseDataSet(data[0])
            else :
                print("No dataset found")
    def deleteDataSet(self): #COMPLETE DELETE OF A DATASET
        if self._ownDataSet():
            data=self._request({"deletedataset":self.id_dataset},'/api/deletedatasetapi/','POST')
            if data['status'] == 'Delete done': 
                print(ss+'dataset deleted')
                self.id_dataset=-1
                self.id_dataset_owner=-1
                self.minTime=-1
                self.maxTime=-1
            else:
                print(strred(' ERROR : '+str(data)))
    def clearDataSet(self): # CLEAR ALL TIME POINT AND INFOS
        if self._ownDataSet():
            data=self._request({"cleardataset":self.id_dataset},'/api/cleardatasetapi/','POST')
            if data['status'] == 'Clear done':  
                print(ss+'dataset cleared')
            else:
                print(strred(' ERROR : '+str(data)))
    
    #MESH
    def _computeCenter(self,obj):
       objA=obj.split("\n")
       X=0.0; Y=0.0; Z=0.0; nb=0;
       for line in objA:
           if len(line)>2 and line[0]=='v' and line[1]!='n'  and line[1]!='t' :
               while line.find("  ")>=0:
                   line=line.replace("  "," ")
               tab=line.strip().split(" ")
               if len(tab)==4:
                   X+=float(tab[1].replace(',','.'))
                   Y+=float(tab[2].replace(',','.'))
                   Z+=float(tab[3].replace(',','.'))
                   nb+=1
       if nb==0:
           print('ERROR your obj does not contains vertex ')
           quit()                
       X/=nb
       Y/=nb
       Z/=nb
       return str(round(X,2))+','+str(round(Y,2))+','+str(round(Z,2))
    def getNumberofMeshAt(self,t,quality=-1,channel=-1):
        if self._ownDataSet():
            data=self._request({"getnumberofmeshat":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/numbermeshapi/','GET')
            ids,ok=tryParseInt(data['nb'])
            if not ok: 
                print(strred(' ERROR : cannot count number of mesh'))
            else :
                return ids
    def clearMeshAt(self,t,quality=-1,channel=-1):
        if self._ownDataSet():
            data=self._request({"clearmeshat":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/clearmeshapi/','POST')
            #data2=json.loads(data)
            if data['status'] == 'Clear done': 
                if quality==-1 and channel==-1:
                    print(ss+'mesh cleared at '+str(t))
                elif quality==-1:
                    print(ss+'mesh cleared at '+str(t)+ " with channel "+str(channel))
                elif channel==-1:
                    print(ss+'mesh cleared at '+str(t)+ " with quality "+str(quality))
                else:
                    print(ss+'mesh cleared at '+str(t)+ " with quality "+str(quality)+ " and channel "+str(channel))
            else:
                print(strred(' ERROR : '+str(data)))


    def uploadMesh(self,t,obj,quality=0,channel=0,link="null",texture=None,material=None,ttype="bmp"): #UPLOAD TIME POINT IN DATASET,new behaviour : do not override existing mesh in database (become uploadMultipleMesh)
        if self._ownDataSet():
            #First we have to upload the texture
            if texture is not None and  material is None:
                print("Please specify the material associate with the texture")
                quit()
            if texture is  None and  material is not None:
                print("Please specify the texture associate with the material")
                quit()
            if obj is None:
                print("The Object file you provided is empty or corrupted, please verify that it is correct")
                return
            id_texture=-1
            if texture is not None and material is not None:
                data=self._large_request({"uploadlargetexture":self.id_dataset,"t":t,"quality":quality,"channel":channel,"type":ttype,"material":material},'/api/uploadtextureapi/',texture)
                id_texture,ok=tryParseInt(data)
                if not ok: 
                    print(strred(' ERROR : texture not upload '+str(data)))
                else :
                    print(ss+"texture at time point "+str(t)+" uploaded ( with id "+str(id_texture)+' )')

            center=self._computeCenter(obj)
            data=self._large_request({"uploadlargemesh":self.id_dataset,"t":t,"quality":quality,"channel":channel,"center":center,"link":link,"id_texture":id_texture},'/api/uploadlargemesh/',obj)
            data2 = json.loads(data)
            ids = -1
            if 'status' in data2: 
                print(strred(' ERROR : time point not uploaded '+str(data)))
            else :
                ids = data2['id']
                print(ss+"meshes at time point "+str(t)+" uploaded ( with id "+str(ids)+' )')
            return ids

    def getMesh(self,t,quality=0,channel=0):
        if self._isDataSet():
            data=self.binary_request({"getmesh":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/getmeshapi/','GET')
            if data is None:
                obj=bz2.decompress(data)
            else :
                print("No mesh found")
                obj = None
            if obj is not None:
                obj = str(obj,'utf-8')
            return obj

    #RAW IMAGES
    def uploadRawImages(self,t,rawdata,channel=0,scale=1):
        if self._ownDataSet():
            if not rawdata.dtype==np.uint8:
                print("Please first convert your data in uint8 ( actually in " + str(rawdata.dtype)+ " ) ")
                quit() 
            data=self._large_request({"uploadlargerawimages":self.id_dataset,"t":t,"channel":channel,"scale":scale,"size":str(rawdata.shape)},'/api/uploadrawimageapi/',rawdata.tobytes(order="F"))
            data2 = json.loads(data)
            if 'status' in data2: 
                print(strred(' ERROR : raw image not uploaded '+str(data)))
            else :
                print(ss+"raw image at time point "+str(t)+" uploaded ( with id "+str(data2['id'])+' )')
            return data2['id']
    def clearRawImages(self):
        if self._ownDataSet():
            data=self._request({"clearrawimages":self.id_dataset},'/api/clearrawimageapi/','POST')
            data2 = json.loads(data)
            if data2['status'] == 'done':  
                print(ss+'rawdata all cleared ')
            else:
                print(strred(' ERROR : '+str(data)))
    def deleteRawImages(self,t,channel=0):
        if self._ownDataSet():
            data=self._request({"deleterawimages":self.id_dataset,"t":t,"channel":channel},'/api/deleterawimageapi/','POST')
            data2 = json.loads(data)
            if data2['status'] == 'done':
                print(ss+'rawdata cleared at '+str(t))
            else:
                print(strred(' ERROR : '+str(data)))

    #PRIMITIVES
    def uploadMeshWithPrimitive(self,t,obj,quality=0,channel=0):
        if self._ownDataSet():
            data=self._large_request({"uploadmeshwithprimitive":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/uploadmeshprimitiveapi/',obj)
            data2 = json.loads(data)
            if 'status' in data2: 
                print(strred(' ERROR : raw image not uploaded '+str(data)))
            else :
                print(ss+"meshes at time point "+str(t)+" uploaded ( with id "+str(data2['id'])+' )')
            return data2['id']

    def uploadPrimitive(self,name,obj):
        if self._ownDataSet():
            data=self._large_request({"uploadprimitive":self.id_dataset,"name":name},'/api/uploadprimitiveapi/',obj)
            data2 = json.loads(data)
            if 'status' in data2: 
                print(strred(' ERROR : raw image not uploaded '+str(data)))
            else :
                print(ss+"primitive "+name+" uploaded ( with id "+str(data2['id'])+' )')
            return data2['id']
    def clearPrimitive(self):
        if self._ownDataSet():
            data=self._request({"clearprimitive":self.id_dataset},'/api/clearprimitiveapi/','POST')
            data2 = json.loads(data)
            if data2['status'] == 'done': 
                print(ss+'primitive all deleted')
            else:
                print(strred(' ERROR : '+str(data)))
    def deletePrimitive(self,name):
        if self._ownDataSet():
            data=self._request({"deleteprimitive":self.id_dataset,"name":name},'/api/deleteprimitiveapi/','POST')
            data2 = json.loads(data)
            if data2['status'] == 'done': 
                print(ss+'primitive '+name+' deleted')
            else:
                print(strred(' ERROR : '+str(data)))



    #INFOS
    def showInfosType(self):
        MorphoFormat={}
        MorphoFormat ["time"] = " objectID:objectID";
        MorphoFormat ["space"] = "objectID:objectID";
        MorphoFormat ["float"] = "objectID:float";
        MorphoFormat ["string"] = "objectID:string";
        MorphoFormat ["group"] = "objectID:string";
        MorphoFormat ["selection"] = "objectID:int";
        MorphoFormat ["color"] = "objectID:r,g,b";
        MorphoFormat ["dict"] = "objectID:objectID:float";
        MorphoFormat ["sphere"] = "objectID:x,y,z,r";
        MorphoFormat ["vector"] = "objectID:x,y,z,r:x,y,z,r";
        print("\nUpload Type : ")
        for s in MorphoFormat:
            print("   "+s+'->'+MorphoFormat[s])
        print('   where objectID : <t,id,ch> or <t,id> or <id>')
        print('\n')
    def listInfos(self):
        if self._isDataSet():
            data=self._request({"listinfos":self.id_dataset},'/api/correspondencelistapi/','GET')
            return data
    def uploadInfos(self,infos,field): 
         if self._isDataSet():
            tab=field.split('\n')
            nbL=0
            datatype=""
            while datatype=="" and nbL<len(tab):
                if len(tab[nbL])>0:
                    types=tab[nbL].split(":")
                    if len(types)==2 and types[0]=="type":
                        datatype=types[1]
                nbL+=1
            if datatype=="":
                self.showInfosType()
                print('You did not specify your type inside the file')
                quit()
            dtype=2 #TYPE =1 For direclty load upload and 2 for load on click
            if datatype=="time" or datatype=="group"  or datatype=="space" :
                dtype=1
            data=self._large_request({"uploadlargecorrespondence":self.id_dataset,"infos":infos,"type":dtype,"datatype":datatype},'/api/uploadinfoapi/',field)
            data2 = json.loads(data)
            ids = -1
            if 'status' in data2: 
                print(strred(' ERROR : info not uploaded '+str(data)))
            else :
                ids = data2['id']
                print(ss+infos+" uploaded (with id "+str(ids)+')')
            return ids
    def deleteInfosByName(self,infos):
        if self._isDataSet():
            data=self._request({"deletecorrespondence":self.id_dataset,"infos":infos},'/api/deleteinfonameapi/','POST')
            ids,ok=tryParseInt(data['id'])
            if not ok: 
                print(strred(' ERROR : '+str(infos)+' '+str(data)))
            else :
                print(ss+infos+" with id "+str(ids)+" deleted")
    def deleteInfosById(self,idinfos):
        if self._isDataSet():
            data=self._request({"deletecorrespondenceid":self.id_dataset,"idinfos":idinfos},'/api/deleteinfoidapi/','POST')
            ids,ok=tryParseInt(data)
            if not ok: 
                print(strred(' ERROR : '+str(idinfos)+' '+str(data)))
            else :
                print(ss+"Infos with id "+str(ids)+" deleted")
    def getInfosByName(self,infos):
        if self._isDataSet():
            data=self.binary_request({"getinfos":self.id_dataset,"infos":infos},'/api/getinfonameapi/','GET')
            #infos=bz2.decompress(data['info'].decode('utf-8'))
            infos=bz2.decompress(data)
            return infos
    def getInfosById(self,idinfos):
        if self._isDataSet():
            data=self.binary_request({"getinfosid":self.id_dataset,"idinfos":idinfos},'/api/getinfoidapi/','GET')
            #infos=bz2.decompress(data['info'].decode('utf-8'))
            infos=bz2.decompress(data)
            return infos
    def _getObjects(self,infos):
        infos=infos.split('\n')
        objects={}
        for line in infos:
            if len(line)>0 and line[0]!="#":
                if line.find("type")==0:
                    dtype=line
                else:
                    tab=line.split(":")
                    objects[tab[0]]=tab[1]
        return objects
    def getObjectsFromInfosId(self,idinfos):
        infos=self.getInfosById(idinfos)
        return self._getObjects(infos)
    def getObjectsFromInfos(self,ninfos):
        infos=self.getInfosByName(ninfos)
        return self._getObjects(infos)




    
        

