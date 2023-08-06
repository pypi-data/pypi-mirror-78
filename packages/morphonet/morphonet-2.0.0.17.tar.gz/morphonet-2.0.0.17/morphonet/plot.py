# -*- coding: latin-1 -*-
import os,sys,errno
import numpy as np
from datetime import datetime
from morphonet.tools import imread,imsave,isfile,copy,getidt,getName
from os.path import isdir,join,dirname,basename

#Class Cell
class MorphoObject():
    def __init__(self,tid):
        tids=tid.split(",")
        self.t =int(tids[0])
        self.id= int(tids[1])
        if len(tids)>2:
            self.s= int(tids[2]) #Selections
    def getName(self):
        return getName(self.t,self.id)


class Dataset():
    def __init__(self,begin,end,raw=None,segment=None,log=True,background=1,pkl_file=None,memory=20):
        self.begin=begin
        self.end=end
        self.log=log
        
        #raw data
        self.raw=False
        self.show_raw=None
        self.raw_datas={}  #list of each rawdata time point  
        if raw is not None:
            self.raw=True
            self.raw_path=dirname(raw)+"/"
            if dirname(raw)=="":
                self.raw_path=""
            self.raw_files=basename(raw)

        #Segmentation
        self.seg_datas={}  #list of each segmented time point 
        self.segment_path=""
        self.segment_files="curated_t{:03d}.inr.gz"
        if segment is not None:
            self.segment_path=dirname(segment)+"/"
            if dirname(segment)=="":
                self.segment_path=""
            self.segment_files=basename(segment)
            if not isdir(self.segment_path):
                os.mkdir(self.segment_path)
        
        #Lineage
        self.lineage_file="lineage.txt"
        self.lineage_file=join(self.segment_path,self.lineage_file)


        #LOG 
        self.log_text="" #Line to log
        if self.log:
            self.log_file=join(self.segment_path,"morpho_log.txt")
    


        self.background=background #Background Color
            
        #DATA Management
        self.memory=memory #Memory to store dataset in Gibabytes
        self.volumes={}
        self.lasT=[] #List of last time step
        self.times=[] #List of modified time point 

        self.lineage=False
        self.lineage_infos={}
        self.pkl_file=pkl_file
        if begin!=end or self.pkl_file is not None:
            self.lineage=True
            self._init_lineage(self.pkl_file) #Lineage Initialisation

        
        self.seeds=None #To Send Centers to Unity

    def add_log(self,txt):
        if self.log:
            self.log_text+=txt

    def save_log(self,command):
        if self.log  and self.log_text!="":
            f=open(self.log_file,"a")
            f.write(str(command)+" #-> "+str(self.log)+" # "+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+"\n")
            f.close()


    def restart(self,command):  #Apply and Restart a Curation 
        print("--> Done " +command)
        self.save_log(command)
        for t in self.times:
            self.save_seg(t)
        MCC=MorphoCurate(self.times)
        MCC.start()
        self.times=[]
    
    #OBJECT ACCESS
    def getObject(*args):
        if len(args) == 2:
            if args[1]=="":
                return None
            return MorphoObject(args[1])
        elif len(args) == 3:
            return MorphoObject(getName(args[1],args[2]))
        return None
        

    ##### DATA ACCESS 
    def _setLast(self,t):
        if t in self.lasT:
            self.lasT.remove(t)
        self.lasT.append(t)
        if t not in self.seg_datas:
            if self._getDataSize()>self.memory*10**9:
                remove_t=self.lasT.pop(0)
                if remove_t in self.seg_datas:
                    del self.seg_datas[remove_t]
                if remove_t in self.raw_datas:
                    del self.raw_datas[remove_t] 

    def _getDataSize(self):
        sif=0
        for t in self.seg_datas:
            if self.seg_datas[t] is not None:
                sif+=self.seg_datas[t].nbytes
        return sif

    def _setVolume(self,data,t):
        #Remove Previous values
        new_volumes={}
        for o in self.volumes:
            if o.t!=t:
                new_volumes[o]=self.volumes[o]
        self.volumes=new_volumes
        #Compute new Volumes
        factor=4 #Computational Factor to reduce ...
        dataResize=data[::factor,::factor,::factor]
        cells=np.unique(dataResize)
        cells=cells[cells!=self.background]
        for c in cells:
            self.volumes[MorphoObject(getName(t,c))]=len(np.where(dataResize==c)[0])*(factor*factor*factor)
        del dataResize
        return self.volumes

    def set_seg(self,t,data):
        self.seg_datas[t]=data
        if t not in self.times:
            self.times.append(t)

    def save_seg(self,t,data=None):
        if data is None:
            data=self.seg_datas[t]
        else:
            self.seg_datas[t]=data
        self._setVolume(data,t)
        if self.log and isfile(join(self.segment_path,self.segment_files.format(t))):
            copy(join(self.segment_path,self.segment_files.format(t)),join(self.segment_path,datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"_"+self.segment_files.format(t)))
        compressed=False
        if not os.path.isfile(join(self.segment_path,self.segment_files.format(t))) and os.path.isfile(join(self.segment_path,self.segment_files.format(t)+".gz")):
            compressed=True
        imsave(join(self.segment_path,self.segment_files.format(t)),data)    
        if compressed:
            os.system("gzip -f "+join(self.segment_path,self.segment_files.format(t))+" &")
    
    def get_raw(self,t):
        self._setLast(t) #Define the time step as used
        if t not in self.raw_datas:
            self.raw_datas[t]=imread(join(self.raw_path,self.raw_files.format(t)))
        return self.raw_datas[t]

    def get_seg(self,t):
        self._setLast(t) #Define the time step as used
        if t not in self.seg_datas:
            self.seg_datas[t]=None
            if isfile(join(self.segment_path,self.segment_files.format(t))):
                self.seg_datas[t]=imread(join(self.segment_path,self.segment_files.format(t)))
        return self.seg_datas[t]

    def getCenter(self,data): #Calculate the center of a dataset
        coords=np.where(data!=self.background)
        center=[coords[0].mean(),coords[1].mean(),coords[2].mean()]
        return center

    #CREATE CENTER TO PLIOT A SPHER
    def addSeed(self,seed):
        if self.seeds is None:
            self.seeds=[]
        self.seeds.append(seed)

    def getSeeds(self):
        if self.seeds is None or len(self.seeds)==0:
            return None
        strseed=""
        for s in self.seeds:
            strseed+=str(s[0])+","+str(s[1])+","+str(s[2])+";"
        self.seeds=None #Reinitializeation
        return strseed[0:-1]

    ##### LINEAGE FUNCTIONS
    def _init_lineage(self,pkl_file):
        if self.lineage_file is not None and os.path.isfile(self.lineage_file):
            self._read_lineage()
        else:
            from morphonet.tools import read_lineage_tree
            if pkl_file is not None and os.path.isfile(pkl_file):
                lin_tree=None
                properties=read_lineage_tree(pkl_file)
                if "lin_tree" in properties:
                    lin_tree=properties["lin_tree"]
                    
                elif 'cell_lineage' in properties:
                    lin_tree=properties["cell_lineage"]
                if lin_tree is None:
                    print("Error readling pkl lineage file, lineage is not present")
                else:
                    #Convert in dictionary form c:m
                    self.lineage_infos={}
                    for idl in lin_tree:
                        t,c=getidt(idl)
                        if t>=self.begin and t<=self.end:
                            for daughter in lin_tree[idl]:
                                td,d=getidt(daughter)
                                self.lineage_infos[MorphoObject(getName(td,d))]=MorphoObject(getName(t,c))

    def _read_lineage(self):
        if self.lineage and os.path.isfile(self.lineage_file):
            self.lineage_infos={}
            f=open(self.lineage_file,"r")
            for line in f:
                if len(line)>0 and line[0]!="#" and line.find("type")==-1:
                    cells=line.split(":")
                    self.lineage_infos[MorphoObject(cells[0])]=MorphoObject(cells[1])
            f.close()

    def _write_lineage(self):
        import pickle
        if self.lineage:
            #Export in MorphoNet Infos
            f=open(self.lineage_file,"w")
            f.write("#Lineage from MorphoCuration generate the "+str(datetime.now())+"\n")
            f.write("type:time\n")
            for c in self.lineage_infos:
                f.write(c.getName()+":"+self.lineage_infos[c].getName()+"\n")
            f.close()

            #Export in PKL
            if self.pkl_file is not None:
                if self.log and isfile(self.pkl_file):
                    copy(self.pkl_file,join(self.segment_path,datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"_"+basename(self.pkl_file)))
                lin_tree_information={}
                for c in self.lineage_infos:
                    m=self.lineage_infos[c]
                    lin_tree_information[c.t*10**4+c.id]=m.t*10**4+m.id
                f=open(self.pkl_file, 'wb')
                pickle.dump(lin_tree_information, f)
                f.close()

    ################## TEMPORAL FUNCTIONS 
    def get_at(self,objects,t):
        cells=[]
        for cid in objects:
            o=self.getObject(cid)
            if o is not None and o.t==t:
                    cells.append(o)
        return cells
    
    def add_link(self,da,mo):
        if self.lineage_infos is None:
            self.lineage_infos={}
        self.lineage_infos[da]=mo

    def del_link(self,o): #We remove all links correspond to a cells
        if self.lineage_infos is not None:
            new_lineage={}
            for c in self.lineage_infos:
                keep=True
                if c.t==o.t and c.id==o.id:
                    keep=False
                d=self.lineage_infos[c]
                if d.t==o.t and d.id==o.id:
                    keep=False
                if keep:
                    new_lineage[c]=self.lineage_infos[c]
            self.lineage_infos=new_lineage
    

#****************************************************************** MORPHONET SERVER
from threading import Thread
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class MorphoInteract():
    def __init__(self):
        self.obj = None  #OBJ To Upload 
        self.cmd=None  #Command to pass (LOAD, DEL )
        self.available = threading.Event() #For Post Waiting function
        self.lock = threading.Event()
        self.lock.set()
    def reset(self):
        self.obj = None  
        self.cmd=None  
        self.available = threading.Event() #Create a new watiing process for the next post request
        self.lock.set() #Free the possibility to have a new command
    def wait(self):  #Wait free request to plot (endd of others requests)
        self.lock.wait()
    def post(self,cmd): #Prepare a command to post
        self.cmd=cmd
        self.lock = threading.Event() #LOCK THE OTHER COMMAND
        self.available.set() 

class MorphoServer(Thread):
    def __init__(self,MCt,host="",port=9875):
        Thread.__init__(self) 
        global MC
        MC=MCt
        self.host=host
        self.port=port
        self.server_address = (self.host, self.port)
    def run(self): #START FUNCTION
        print("Run server Localhost on the port ", self.port)
        self.httpd = HTTPServer(self.server_address, MorphoHTTPRequestHandler)
        self.httpd.serve_forever()
    def stop(self):
        self.httpd.shutdown()

class MorphoHTTPRequestHandler(BaseHTTPRequestHandler):
 
    def do_GET(self): #NOT USED
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*") #To accept request from morphonet
        self.end_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        global inter,MC
        from urllib.parse import unquote
        from io import BytesIO
        #print(" Wait for a post")
        inter.available.wait() #Wait the commnand available
        #print(" Command IS "+self.segment_path)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*") #To accept request from morphonet
        self.end_headers()
        response = BytesIO()
        if self.path.find("done")>=0 :
            #print("Close command from client")
            response.write(bytes("DONE", 'utf-8'))
            inter.reset() #FREE FOR OTHERS COMMAND
        elif self.path.find("send")>=0 : #ANNOTATION ARE SEND !
            #print("Recieve Annotations from client")
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            command =self.rfile.read(content_length)
            #print(post_data)
            actions=unquote(str(command.decode('utf-8'))).split("&")
            action=actions[0][actions[0].index("=")+1:]
            current_time=int(actions[1][actions[1].index("=")+1:])
            objects=actions[2][actions[2].index("=")+1:].strip().split(";")
            response.write(bytes("DONE", 'utf-8'))
            #print("action="+action)
            if action=="showraw":
                MC.plot_raws(current_time)
            elif action=="upload":
                MC.upload(objects[0],2)
            else:
                for plug in MC.plugins:
                    if plug.cmd()==action: #print(" Found Plugin "+plug().cmd())
                        ifo=0 
                        for tf in plug.inputfields:
                            plug.set_InputField(tf,actions[3+ifo][actions[3+ifo].index("=")+1:])
                            ifo+=1
     
                        for dd in plug.dropdowns:
                            plug.set_Dropdown(dd,actions[3+ifo][actions[3+ifo].index("=")+1:])
                            ifo+=1

                        for cd in plug.coordinates:
                            plug.set_Coordinates(cd,actions[3+ifo][actions[3+ifo].index("=")+1:])
                            ifo+=1

                        plug.process(current_time,MC.dataset,objects)
            inter.reset() #FREE FOR OTHERS COMMAND
        elif inter.cmd is not None : #SEND DATA
            #print("Send Response to server for "+inter.cmd)
            response.write(bytes(inter.cmd, 'utf-8'))
            response.write(b';') #ALWAYS ADD A SEPARATOR
            if inter.obj is not None:
                if  inter.cmd.find("RAW")==0:
                    response.write(inter.obj)
                else :
                    response.write(bytes(inter.obj, 'utf-8'))
        self.wfile.write(response.getvalue())

    def log_message(self, format, *args):
        return
    
class Plot:#LOCAL SERVER TO COMMUNICATE DIRECTLY WITH UNITY
    def __init__(self,log=True,start_browser=True): 
        global inter
        inter=MorphoInteract()
        self.unity_connection=MorphoServer(self) #Instantiate the local MorphoNet server 
        self.unity_connection.start() #Start it 
        if start_browser :
            self.showBrowser()
        self.plugins=[]
        self.log=log
    
    def connect(self, login,passwd): #Need to be connected to be upload on MorphoNet 
        import morphonet 
        self.mn=morphonet.Net(login,passwd)

    def upload(self,dataname,upload_factor=2):
        from morphonet.tools import convertToOBJ
        print("---->>> Upload dataset "+dataname)
        self.mn.createDataSet(dataname,minTime=self.dataset.begin,maxTime=self.dataset.end)
        for t in range(self.dataset.begin,self.dataset.end+1):
            data=self.dataset.get_seg(t)
            if data is not None:
                obj=convertToOBJ(data,t,background=self.dataset.background,factor=upload_factor)
                self.mn.uploadMesh(t,obj)
        #TODO add Infos
        print("---->>>  Uploading done")

    #Define a dataset 
    def setDataset(self,begin=0,end=0,raw=None,segment=None,background=1,pkl_file=None,factor=4,raw_factor=4,memory=20):
        self.dataset=Dataset(begin,end,raw=raw,segment=segment,log=self.log,background=background,pkl_file=pkl_file,memory=memory)
        self.center=None
        self.factor=factor #Reduce factor to compute the obj
        self.raw_factor=raw_factor #Reduction factor
        
    #Add A plugin
    def add_plugin(self,plug):
        self.plugins.append(plug)
        self.create_plugin(plug)


    def create_plugin(self,plug):
        global inter
        inter.wait()
        print(" --> create Plugin "+plug.name)
        inter.obj=plug.getBtn()
        inter.post("BTN")
        
    def set_default_plugins(self):
        from morphonet.plugins import defaultPlugins
        for plug in defaultPlugins:
            self.add_plugin(plug)
    
    ##### OPEN FIREFOX BROWSER
    def showBrowser(self): 
        import webbrowser
        from morphonet import url
        print("open "+url)
        try:
            webbrowser.get('firefox').open_new_tab("http://"+url+'/morphoplot')
        except Exception as e:
            print("Firefox error: " % e)
            quit()

    ##### SERVER FUNCTIONS
    def quit(self):
        #We have to wait to be free 
        global inter
        inter.available.wait()
        self.unity_connection.stop() #Shut down the server

    def curate(self): #START UPLOAD AND WAIT FOR ANNOTATION
        if len(self.plugins)==0: #Initialise Default set of plugins
            self.set_default_plugins()

        self.plot_meshes()
        self.plot_volumes()
        self.plot_lineage()

        self._annotate()


    ##### RAWIMAGES FUNCTIONS
    def plot_raws(self,t):
        if self.dataset.raw:
            if self.dataset.show_raw is None or self.dataset.show_raw!=t:
                self.dataset.show_raw=t
                self.dataset.restart("showraw")         

    def plot_raw(self,t):
        if self.dataset.raw:
            global inter
            print(" Send rawdatas at "+str(t))
            rawdata=self.dataset.get_raw(t)
            new_shape=np.uint16(np.floor(np.array(rawdata.shape)/self.raw_factor)*self.raw_factor) #To avoid shifting issue
            rawdata=rawdata[0:new_shape[0],0:new_shape[1],0:new_shape[2]]
            factor_data=rawdata[::self.raw_factor,::self.raw_factor,::self.raw_factor]
            bdata=np.uint8(np.float32(np.iinfo(np.uint8).max)*factor_data/factor_data.max()).tobytes(order="F")        
            inter.wait()
            inter.obj=bdata
            if self.center is None:
                self.center=[np.round(rawdata.shape[0]/2),np.round(rawdata.shape[1]/2),np.round(rawdata.shape[2]/2)]
            cmd="RAW_"+str(t)+"_"+str(rawdata.shape[0])+"_"+str(rawdata.shape[1])+"_"+str(rawdata.shape[2])+"_"+str(self.raw_factor)+"_"+self._getCenterText()
            inter.post(cmd)


    ###### ADDD CENTERS
    def plot_seeds(self,seeds):
        if seeds is not None and seeds!="":
            global inter
            inter.wait()
            inter.obj=seeds
            inter.post("SEEDS")

    ##### PRIMITIVES FUNCTIONS 
    def addPrimitive(self,name,obj): #UPLOAD DITECLTY THE OBJ TIME POINT IN UNITY
        global inter
        inter.wait()
        inter.obj=obj
        inter.post("PRIM_"+str(name))

    ##### INFOS FUNCTIONS
    def _create_infos(self,inf,info_type,name_plot):
        MainComments="#Interactive Plot"+'\n'
        Text=MainComments+'#'+name_plot+'\n'
        Text+="type:"+info_type+"\n"
        for o in inf:
            if o.t>=self.dataset.begin and o.t<=self.dataset.end:
                if info_type=="float" or info_type=="string":
                    Text+=o.getName()+':'+str(inf[o])+'\n'
                elif info_type=="time":
                    Text+=o.getName()+':'+inf[o].getName()+'\n'
        return Text

    def plot_infos(self,infoname,infos): #PLOT INFOR (CORRESPONDENCAE)
        if len(infos.split('\n'))>4:
            global inter
            inter.wait() #Wait free request to plot
            inter.obj=infos
            inter.post("INFO_"+infoname.replace(" ","_"))
 
    def plot_lineage(self):
        if self.dataset.lineage:
            info=self._create_infos(self.dataset.lineage_infos,"time","Lineage")
            self.plot_infos("Lineage",info)

    def plot_volumes(self):#### CALCUL VOLUMES
        info=self._create_infos(self.dataset.volumes,"float","Volumes")
        self.plot_infos("Volumes",info)


    ##### INTERACTIVE INTERNAL FUNCTIONS
    def _annotate(self): #WAIT FOR A SEND ANNOTATION
        global inter
        inter.wait()
        inter.reset()  
        inter.post("ANNOTATE_"+str(self.dataset.begin)+"_"+str(self.dataset.end))


    def _getCenterText(self):
        if self.center is not None:
            return str(int(round(self.center[0])))+"_"+str(int(round(self.center[1])))+"_"+str(int(round(self.center[2])))
        return "0_0_0"

    ##### MESH FUNCTIONS
    def _get_mesh(self,t,data):
        from morphonet.tools import convertToOBJ
        if self.center is None:
            self.center=self.dataset.getCenter(data)
        obj=convertToOBJ(data,t,background=self.dataset.background,factor=self.factor,center=self.center) #Create the OBJ
        return obj  
    
    def plot_mesh(self,t): #UPLOAD DITECLTY THE OBJ TIME POINT IN UNITY
        global inter
        inter.wait()
        data=self.dataset.get_seg(t)
        print(" ->  Send mesh at "+str(t))
        if data is not None:
            self.dataset._setVolume(data,t) #Update Volumes
            inter.obj=self._get_mesh(t,data)
        else:
            inter.obj=""
        inter.post("LOAD_"+str(t))

    def plotAt(self,t,obj):#PLOT DIRECTLY THE OBJ PASS IN ARGUMENT
        global inter
        inter.wait()
        inter.obj=obj
        inter.post("LOAD_"+str(t))

    def plot_meshes(self):  # PLOT ALL THE TIMES STEP EMBRYO IN MORPHONET
        for t in range(self.dataset.begin,self.dataset.end+1):
            self.plot_mesh(t)
           
    def del_mesh(self,t): #DELETE DITECLTY THE OBJ TIME POINT IN UNITY
        global inter
        inter.wait()
        inter.post("DEL_"+str(t))

class MorphoCurate(Thread):
    def __init__(self,ts_seg):
        Thread.__init__(self) 
        self.ts_seg=ts_seg #List of modified t
    def run(self): #START FUNCTION
        global MC
        if self.ts_seg is not None: #PLOT MESHES
            for t in self.ts_seg:
                MC.plot_mesh(t)
        if MC.dataset.show_raw is not None: #PLOT RAWDATAS
            MC.plot_raw(MC.dataset.show_raw)
        MC.plot_seeds(MC.dataset.getSeeds())
        
        MC.dataset._write_lineage()
        MC.plot_volumes()
        MC.plot_lineage()
        MC._annotate()
        print(">>>>>>> Go back on MorphoNet ")



