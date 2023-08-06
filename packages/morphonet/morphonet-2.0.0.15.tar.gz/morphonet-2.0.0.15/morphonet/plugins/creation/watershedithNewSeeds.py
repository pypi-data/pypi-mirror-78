# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


# Test if a center is inside the image
def centerInShape(c,s): 
    if c[0]<0 or c[1]<0 or c[2]<0 or c[0]>=s[0] or c[1]>=s[1] or c[2]>=s[2]:
        return False 
    return True




#Add an new object based on a new seed 
class watershedithNewSeeds(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Watershed")
        self.add_Coordinates("Add a Seed")
        self.set_Parent("Create new objects")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        seeds=self.get_Coordinates("Add a Seed")
        print(" ------>> Process "+self.name+" at "+ str(t) + " with "+str(len(seeds))+ " new seeds")
        from skimage.morphology import label,watershed
        import numpy as np
        data=dataset.get_seg(t)
        center=dataset.getCenter(data)

        #First we remove seeds which are inside other cell 
        new_seed=[]
        for s in seeds:
            seed=np.int32(s+center)
            if centerInShape(seed,data.shape):
                olid=data[seed[0],seed[1],seed[2]]
                if olid==dataset.background: 
                    new_seed.append(seed)
                else:
                    print(" ----> remove this seed "+str(seed)+ " which already correspond to cell "+str(olid))
            else:
                print("Center "+str(seed)+ " is out of the image")

        if len(new_seed)>0:                 
            rawdata=dataset.get_raw(t)
            factor=4 #Reduce Factor to go faster  (TODO  depend on the size of the iamge...)
            dataF=data[::factor,::factor,::factor] #To go faster...

            cells=np.unique(dataF)
            cells=cells[cells!=dataset.background]

            markers=np.zeros(data.shape,dtype=np.uint16)
            markers[0,:,:]=dataset.background
            markers[:,0,:]=dataset.background
            markers[:,:,0]=dataset.background
            markers[data.shape[0]-1,:,:]=dataset.background
            markers[:,data.shape[1]-1,:]=dataset.background
            markers[:,:,data.shape[2]-1]=dataset.background

            for c in cells:  #For each Cell
                coord=np.where(dataF==c) 
                bary=np.int32([factor*coord[0].mean(),factor*coord[1].mean(),factor*coord[2].mean()])
                markers[bary[0],bary[1],bary[2]]=c

            newId=cells.max()+1
            for seed in new_seed: #For Each Seeds ...
                print("--> add seed "+str(seed)+' with id '+str(newId))
                markers[seed[0],seed[1],seed[2]]=newId
                newId+=1
            
            #Create The Mask
            mask=np.ones(data.shape,dtype=np.bool)
            mask[data!=dataset.background]=False
                
            print("--> Process watershed ")
            labelw=watershed(rawdata,markers, mask=mask)
            labelw[np.where(data!=dataset.background)]=dataset.background
            new_ids=np.unique(labelw)
            new_ids=new_ids[new_ids>cells.max()]
            print("--> Found  "+str(new_ids)+" new labels")
            for new_id in new_ids:
                newIdCoord=np.where(labelw==new_id)
                data[newIdCoord]=new_id
                dataset.add_log("add_"+str(t)+','+str(new_id)+";")
                dataset.set_seg(t,data)
        
        dataset.restart(self.name)
