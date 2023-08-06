# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin


#Create links with objects in time
class addTemporalLink(MorphoPlugin):
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_Name("Create Links")
        self.set_Parent("Temporal Relation")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        print(" ------>> Process "+self.name+" for "+str(objects) )
        times=[]  #List all times
        for cid in objects:
            o=dataset.getObject(cid)
            if o is not None and o.t not in times:
                times.append(o.t)
        times.sort() #Order Times

        for t in times:
            if t+1 in times:
                cellT=dataset.get_at(objects,t)
                cellTP=dataset.get_at(objects,t+1)
                for daughter in cellTP:
                    for mother in cellT:
                        dataset.add_link(daughter,mother)
                        dataset.add_log("link_"+daughter.getName()+":"+mother.getName()+";")
        dataset.restart(self.name)
