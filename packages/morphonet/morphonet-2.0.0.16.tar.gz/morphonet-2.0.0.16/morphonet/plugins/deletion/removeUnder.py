# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin

#Remove Small Voxels Element under a certain size for all time points
class removeUnder(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Remove Under")
        self.set_Parent("Remove objects")
        self.add_InputField("Voxel Size",20)

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if self.get_InputField("Voxel Size") is None:
            print("Please fill the parameters ")
        else:
            print(" ------>> Process "+self.name+" under "+str(self.get_InputField("Voxel Size"))+ " voxels")
            import numpy as np
            for t in range(dataset.begin,dataset.end+1):
                print("     ----->>>  Process "+self.name+" at "+str(t))
                data=dataset.get_seg(t)
                cells=np.unique(data)
                cells=cells[cells!=dataset.background]
                for c in cells:
                    coords=np.where(data==c)
                    nb=len(coords[0])
                    if nb<float(self.get_InputField("Voxel Size")):
                         print("     ----->>>  delete object "+str(c)+" at "+str(t) + " with "+str(nb)+" pixels")
                         data[coords]=dataset.background
                         o=dataset.getObject(t,c)
                         dataset.add_log("del_"+o.getName()+";")
                         dataset.del_link(o)
                         dataset.set_seg(t,data)
                  
        dataset.restart(self.name) #ADD At the end 
         




