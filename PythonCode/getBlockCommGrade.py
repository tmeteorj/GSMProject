import time
import random
import os
import psutil
def timeEvaluation(solvecnt,totalcnt,costtime):
    avetime=costtime/solvecnt
    remaintime=avetime*(totalcnt-solvecnt)
    hour=remaintime//3600
    minu=remaintime%3600/60
    secs=int(remaintime%60)
    return max(hour,0),max(0,minu),max(0,secs)
def memUsed():
    m=psutil.virtual_memory()
    return m.percent,m.used,m.total
def countline(filePath,sizeF=-1):
    count=0
    f=open(filePath,"rb")
    sol=0
    sizeF=os.path.getsize(filePath)/1024/1024/1024
    while True:
        buff=f.read(1024*1024*1024)
        if not buff:break
        sol+=1
        count+=buff.count("\n")
        if sol==2 and sizeF!=-1:
            count=int(count/2.0*sizeF)
            break
    f.close()
    return count
def loadPeoplePlane(inputpath):
    global peoplebelong
    peoplebelong=dict()
    for line in open(inputpath,"r"):
        if line.find("null")!=-1:continue
        info=line.strip().split(",")
        peoplebelong[info[0]]=info[1]
def loadPlaneStatical(pcountpath):
    global planestat
    planestat=dict()
    for line in open(pcountpath,"r"):
        info=line.strip().split(",")
        planestat[info[0]]=dict()
        planestat[info[0]]["com"]=set()
        planestat[info[0]]["count"]=int(info[1])
def planeComCount(compath,outputpath):
    global planestat,peoplebelong
    for line in open(compath,"r"):
        info=line.strip().split(",")
        pid=peoplebelong[info[0]]
        planestat[pid]["com"].add(info[1])
    fw=open(outputpath,"w")
    for pid in planestat:
        fw.write("%s,%d,%d\n"%(pid,len(planestat[pid]["com"]),planestat[pid]["count"]))
    fw.close()
def clearset():
    global planestat
    for pid in planestat:
        planestat[pid]["com"]=set()
if __name__=="__main__":
    for mon in range(201409,201412):
       loadPeoplePlane("home2014/phome"+str(mon)+".txt")
       loadPlaneStatical("home2014/pcount"+str(mon)+".txt")
       planeComCount("e2014/socialnode"+str(mon)+".txt","e2014/planesocialnode"+str(mon)+".txt")
       clearset()
       planeComCount("e2014/distsocialnode"+str(mon)+".txt","e2014/planedistnode"+str(mon)+".txt")
       clearset()
       planeComCount("e2014/gravsocialnode"+str(mon)+".txt","e2014/planegravnode"+str(mon)+".txt")

