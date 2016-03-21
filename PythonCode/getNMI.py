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
def loadPeoplePlane(inputpath):
    global usercom
    print("Start loadPeoplePlane("+inputpath+")")
    usercom=dict()
    for line in open(inputpath,"r"):
        if line.find("null")!=-1:continue
        info=[int(t) for t in line.strip().split(",")]
        usercom[info[0]]=[info[1],-1,-1,-1]
    print("Completed loadPeoplePlane("+inputpath+")")
def loadPlaneCount(inputpath):
    global peoplecount
    print("Start loadPlaneCount("+inputpath+")") 
    peoplecount=dict()
    for line in open(inputpath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        peoplecount[info[0]]=info[1]
    print("Completed loadPlaneCount("+inputpath+")")
def loadCom(inputpath,col):
    global usercom
    print("Start loadCom("+inputpath+")") 
    for line in open(inputpath,"r"):
        #user,comid
        info=[int(t) for t in line.strip().split(",")]
        usercom[info[0]][col]=info[1]
    print("Completed loadCom("+inputpath+")")
def getComNMI(a,b):
    global usercom
    pa=dict()
    pb=dict()
    pab=dict()
    tot=float(len(usercom))
    solvecnt=0
    totalcnt=tot*4
    starttime=time.time()
    for u in usercom:
        x=usercom[u][a]
        y=usercom[u][b]
        xy=str(x)+","+str(y)
        pa[x]=1 if x not in pa else pa[x]+1
        pb[y]=1 if y not in pb else pb[y]+1
        pab[xy]=1 if xy not in pab else pab[xy]+1
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("getComNMI[%d,%d], count..., remain %02d:%02d:%02d"%(a,b,h,m,s))
    mi=0.0
    ha=0.0
    hb=0.0
    solvecnt+=tot-len(pa)
    for x in pa:
        ha-=pa[x]/tot*math.log(pa[x]/tot)
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("getComNMI[%d,%d], count..., remain %02d:%02d:%02d"%(a,b,h,m,s))
    solvecnt+=tot-len(pb)
    for y in pb:
        hb-=pb[y]/tot*math.log(pb[y]/tot)
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("getComNMI[%d,%d], count..., remain %02d:%02d:%02d"%(a,b,h,m,s))
    solvecnt+=tot-len(pab)
    for xy in pab:
        info=[int(t) for t in xy.split(",")]
        x=info[0]
        y=info[1]
        mi+=pab[xy]/tot*math.log(pab[xy]*tot/(pa[x]*pb[y]))
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("getComNMI[%d,%d], count..., remain %02d:%02d:%02d"%(a,b,h,m,s))
    return 2*mi/(ha+hb)
def getPlaneNMI(a,b,outputpath):
    global usercom,peoplecount
    lastplane=-1
    solvecnt=0
    totalcnt=len(usercom)
    starttime=time.time()
    result=dict()
    for user in sorted(usercom.items(),key=lambda arg:arg[1][0]):
        item=user[1]
        if(item[a]==-1 or item[b]==-1):continue
        if item[0]!=lastplane:
            if lastplane!=-1:
                ha=0.0
                hb=0.0
                mi=0.0
                tot=float(peoplecount[lastplane])
                for x in pa:ha-=pa[x]/tot*math.log(pa[x]/tot)
                for y in pb:hb-=pb[y]/tot*math.log(pb[y]/tot)
                for xy in pab:
                    info=[int(t) for t in xy.split(",")]
                    x=info[0]
                    y=info[1]
                    mi+=pab[xy]/tot*math.log(pab[xy]*tot/(pa[x]*pb[y]))
                if(mi>0 or ha>0 or hb>0):
                    nmi=2*mi/(ha+hb)
                    result[lastplane]=nmi
            pa=dict()
            pb=dict()
            pab=dict()
        x=item[a]
        y=item[b]
        xy=str(x)+","+str(y)
        pa[x]=1 if x not in pa else pa[x]+1
        pb[y]=1 if y not in pb else pb[y]+1
        pab[xy]=1 if xy not in pab else pab[xy]+1
        lastplane=item[0]
    if lastplane!=-1:
        ha=0.0
        hb=0.0
        mi=0.0
        tot=float(peoplecount[lastplane])
        for x in pa:ha-=pa[x]/tot*math.log(pa[x]/tot)
        for y in pb:hb-=pb[y]/tot*math.log(pb[y]/tot)
        for xy in pab:
            info=[int(t) for t in xy.split(",")]
            x=info[0]
            y=info[1]
            mi+=pab[xy]/tot*math.log(pab[xy]*tot/(pa[x]*pb[y]))
        if(mi>0 or ha>0 or hb>0):
            nmi=2*mi/(ha+hb)
            result[lastplane]=nmi
    fw=open(outputpath,"w")
    for x in sorted(result.items(),key=lambda arg:arg[1]):
        fw.write("%d,%.6f\n"%(x[0],x[1]))
    fw.close()
if __name__=="__main__":
    fw=open("MaxCP_NMI_Compare.txt","w")
    fw.write("month,social2plane,dist2plane,grav2plane,social2dist,social2grav,dist2grav\n")
    for mon in range(201409,201412):
        loadPlaneCount("home2014/pcount"+str(mon)+".txt")
        loadPeoplePlane("home2014/phome"+str(mon)+".txt")
        loadCom("e2014/maxcpsocialnode"+str(mon)+".txt",1)
        loadCom("e2014/maxcpdistsocialnode"+str(mon)+".txt",2)
        loadCom("e2014/maxcpgravsocialnode"+str(mon)+".txt",3)
        getPlaneNMI(0,1,"statistical2014/maxcp_zone_social2plane.csv")
        getPlaneNMI(0,2,"statistical2014/maxcp_zone_dist2plane.csv")
        getPlaneNMI(0,3,"statistical2014/maxcp_zone_grav2plane.csv")
        getPlaneNMI(1,2,"statistical2014/maxcp_zone_social2dist.csv")
        getPlaneNMI(1,3,"statistical2014/maxcp_zone_social2grav.csv")
        getPlaneNMI(2,3,"statistical2014/maxcp_zone_dist2grav.csv")
        s2p=getComNMI(0,1)
        d2p=getComNMI(0,2)
        g2p=getComNMI(0,3)
        s2d=getComNMI(1,2)
        s2g=getComNMI(1,3)
        d2g=getComNMI(2,3)
        fw.write("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n"%(mon,s2p,d2p,g2p,s2d,s2g,d2g))
    fw.close()
