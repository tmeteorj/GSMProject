import time
import random
import os
import psutil
import math
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
def countline(filePath):
    count=0
    f=open(filePath,"rb")
    sol=0
    sizeF=os.path.getsize(filePath)/1024/1024/1024
    while True:
        buff=f.read(1024*1024*1024)
        if not buff:break
        sol+=1
        count+=buff.count("\n")
        if sol==2:
            count=int(count/2.0*sizeF)
            break
    f.close()
    return count
def loadPlaneInfo(inputpath):
    global plane
    plane=dict()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        #plane[pid]=[Attrbute,Area,Population,Density_p,Scnt,Dcnt,Gcnt,Density_S,Density_D,Density_G,SD,SG,SP,DG,DP,GP]
        plane[info[0]]=[info[1],info[2],-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
def loadPeopleCount(inputpath):
    global plane
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        if info[1]=='0':continue
        plane[info[0]][2]=info[1]
        plane[info[0]][3]=float(info[1])/float(plane[info[0]][1])*1000000
def loadCommunityCount(inputpath,index):
    global plane
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        if info[1]=="0":continue
        plane[info[0]][index]=info[1]
        plane[info[0]][index+3]=float(info[1])/float(plane[info[0]][2])
def loadNMICount(inputpath,index):
    global plane
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        plane[info[0]][index]=info[1]
def loadPlaneWithout(inputpath,outputpath):
    fw=open(outputpath,"w")
    for line in open(inputpath,"r"):
        if line.find("-1")!=-1:continue
        fw.write(line)
    fw.close()
def run():
    for mon in range(201409,201412):
        loadPlaneInfo("PlaneInfo.csv")
        loadPeopleCount("home2014/pcount"+str(mon)+".txt")
        loadCommunityCount("e2014/planesocialnode"+str(mon)+".txt",4)
        loadCommunityCount("e2014/planedistnode"+str(mon)+".txt",5)
        loadCommunityCount("e2014/planegravnode"+str(mon)+".txt",6)
        loadNMICount("statistical2014/maxcp_zone_social2dist"+str(mon)+".txt",10)
        loadNMICount("statistical2014/maxcp_zone_social2grav"+str(mon)+".txt",11)
        loadNMICount("statistical2014/maxcp_zone_social2plane"+str(mon)+".txt",12)
        loadNMICount("statistical2014/maxcp_zone_dist2grav"+str(mon)+".txt",13)
        loadNMICount("statistical2014/maxcp_zone_dist2plane"+str(mon)+".txt",14)
        loadNMICount("statistical2014/maxcp_zone_grav2plane"+str(mon)+".txt",15)
        outputPlane("plane2014/planeAttr"+str(mon)+".txt")
if __name__=="__main__":
    for mon in range(201409,201412):
        loadPlaneWithout("plane2014/planeAttr"+str(mon)+".txt","plane2014/WithoutPlaneAttr"+str(mon)+".txt")
