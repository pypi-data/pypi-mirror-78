# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

#Delete a list of selected objects
class deleteSelectedObjects(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Delete")
        self.set_Parent("Remove objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        print(" ------>> Process "+self.name +" "+str(objects))
        import numpy as np
        for cid in objects:
            if cid!="":
                o=dataset.getObject(cid)
                data=dataset.get_seg(o.t)
                print(" --> delete object "+str(o.id)+" at "+str(o.t))
                dataset.add_log("del_"+o.getName()+";")
                dataset.del_link(o)
                data[np.where(data==o.id)]=dataset.background
                dataset.set_seg(o.t,data)
           
        dataset.restart(self.name)





