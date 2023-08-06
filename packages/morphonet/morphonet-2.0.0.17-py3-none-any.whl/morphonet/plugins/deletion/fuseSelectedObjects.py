# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

#Fuse selected objects in one
class fuseSelectedObjects(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Fuse")
        self.set_Parent("Remove objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        print(" ------>> Process "+self.name+" "+str(objects))
        import numpy as np
        times=[]
        for cid in objects: #List all time points
            o=dataset.getObject(cid)
            if o is not None and o.t not in times:
                times.append(o.t)

        for t in times:
            tofuse={}
            for cid in objects:
                o=dataset.getObject(cid)
                if o is not None and o.t==t: 
                    if o.s not in tofuse:
                        tofuse[o.s]=[]
                    tofuse[o.s].append(o.id)
            for s in tofuse:
                if len(tofuse[s])>1 : #More than one object to fuse..
                    data=dataset.get_seg(t)
                    minFuse=np.array(tofuse[s]).min()
                    print(" --> fuse objects "+str(tofuse[s])+" at "+str(t) + " in "+str(minFuse))
                    dataset.add_log("fuse_"+str(t)+","+str(minFuse)+";")
                    for tof in tofuse[s]:
                        if tof!=minFuse:
                            data[np.where(data==tof)]=minFuse
                            dataset.del_link(dataset.getObject(t,tof)) 
                    dataset.set_seg(t,data)

        dataset.restart(self.name)



