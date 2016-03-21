import time
import random
import os
import psutil
def timeEvaluation(solvecnt,totalcnt,costtime):
    totalcnt=max(solvecnt,totalcnt)
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
def loadDistanceOD(planedistpath):
    global od,pn
    print("Start load "+planedistpath)
    od=dict()
    pn=dict()
    pid=0
    for line in open(planedistpath,"r"):
        info=line.strip().split(",")
        pn[info[0]]=pid
        od[pid]=list()
        for item in info[(2+pid):]:
            od[pid].append(float(item))
        pid+=1
    print("End load "+planedistpath)
def loadPlaneCount(planepath):
    global pc
    pc=dict()
    print("Start load "+planepath)
    for line in open(planepath):
        info=line.strip().split(",")
        pc[info[0]]=int(info[1])
    print("End load "+planepath)
def getGravNetwork(userplanepath,networkpath,outputpath):
    global od,pn,pc
    print("Start load "+userplanepath)
    up=dict()
    for line in open(userplanepath,"r"):
        if line.find("null")!=-1:continue
        info=line.strip().split(",")
        up[info[0]]=info[1]
    print("End load "+userplanepath)
    fw=open(outputpath,"w")
    solvecnt=0
    totalcnt=countline(networkpath)
    starttime=time.time()
    ratecnt=max(totalcnt/10000,1)
    for line in open(networkpath,"r"):
        info=line.strip().split(",")
        ci=list()
        pi=list()
        for item in info[:2]:
            pi.append(pn[up[item]])
            ci.append(pc[up[item]])
        a=min(pi[0],pi[1])
        b=max(pi[0],pi[1])
        if a==b or od[a][b-a-1]<1:d=1
        else:d=od[a][b-a-1]
        g=float(info[2])*ci[0]*ci[1]/d/d
        fw.write("%s,%s,%.4f\n"%(info[0],info[1],g))
        solvecnt+=1
        if random.random()*ratecnt<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("getGravNetwork(%s): %d/%d->%.4f%%, %02d:%02d:%02d"%(networkpath,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    fw.close()
if __name__=="__main__":
    loadDistanceOD("DistanceOD.txt")
    for mon in range(201409,201412):
        loadPlaneCount("home2014/pcount"+str(mon)+".txt")
        getGravNetwork("home2014/phome"+str(mon)+".txt","e2014/subnet"+str(mon)+".txt","e2014/gravnet"+str(mon)+".txt")

