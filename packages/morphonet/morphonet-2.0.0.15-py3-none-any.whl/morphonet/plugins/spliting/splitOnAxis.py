# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


#Split selected objects in a specitifc Axis
class splitOnAxis(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Split On Axis")
        self.add_Dropdown("Axis",["X","Y","Z"])
        self.set_Parent("Split objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        print(" ------>> Process "+self.name+" on "+str(objects))
        import numpy as np
        which=self.get_Dropdown("Axis")
        xyz=-1
        if which=="X":
            xyz=0
        elif which=="Y":
            xyz=1
        elif which=="Z":
            xyz=2
        if xyz==-1:
            print('ERROR' + which+ " unknown ....")
        else:
            for cid in objects:
                o=dataset.getObject(cid)
                if o is not None:
                    dataset.add_log("split_"+o.getName()+";")
                    print('     ----->>>  Split Object '+str(o.getName())+ " in "+str(which))
                    data=dataset.get_seg(o.t)
                    coords=np.where(data==o.id)
                    xyzList=np.unique(coords[xyz])
                    xyzList.sort()
                    lastID=data.max()
                    lastID=lastID+1
                    w=np.where(coords[xyz]>int(xyzList.mean()))
                    new_coords=(coords[0][w],coords[1][w],coords[2][w])
                    data[new_coords]=lastID
                    print('     ----->>>>>  Create a new ID '+str(lastID)+ " with "+str(len(new_coords[0]))+ " pixels")
                    dataset.set_seg(t,data)

        dataset.restart(self.name)
