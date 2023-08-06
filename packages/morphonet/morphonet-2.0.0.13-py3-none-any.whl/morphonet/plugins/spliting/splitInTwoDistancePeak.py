# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from .functions import *

#Split Selected Objects based on Distance between Two Peaks in Segmentation Cells  -> GOOD to separate 2 fused cells
class splitInTwoDistancePeak(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Split In 2")
        self.set_Parent("Split objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        print(" ------>> Process "+self.name+" "+str(objects))
        from scipy import ndimage as ndi 
        from skimage.morphology import label,watershed
        from skimage.feature import peak_local_max
        import numpy as np
        for cid in objects:
            o=dataset.getObject(cid)
            if o is not None:
                dataset.add_log("split_"+o.getName()+";")
                print('     ----->>>  Split Object '+str(o.getName()))
                data=dataset.get_seg(o.t)
                cellCoords=np.where(data==o.id)
                xmin,xmax,ymin,ymax,zmin,zmax=getBorders(data,cellCoords)
                cellShape=[1+xmax-xmin,1+ymax-ymin,1+zmax-zmin]
                mask=np.zeros(cellShape,dtype=np.bool)
                mask[cellCoords[0]-xmin,cellCoords[1]-ymin,cellCoords[2]-zmin]=True
                distance = ndi.distance_transform_edt(mask)
                local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3, 3)),num_peaks=2)
                markers = ndi.label(local_maxi)[0]
                labelw = watershed(-distance, markers, mask=mask)
                data=applyNewLabel(data,xmin,ymin,zmin,labelw)
                dataset.del_link(o)
                dataset.set_seg(t,data)
                
        dataset.restart(self.name)
