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
def find(x):
    global fa
    if x not in fa:fa[x]=x
    if fa[x]==x:return x
    else:
        fa[x]=find(fa[x])
        return fa[x]
def makeset(x,y):
    global fa
    fx=find(x)
    fy=find(y)
    if fx<fy:fa[fy]=fx
    elif fx>fy:fa[fx]=fy
def subgraphinfo(inputpath,outputpath,comsizepath):
    global fa
    fa=dict()
    solvecnt=0
    totalcnt=countline(inputpath)
    ratecnt=totalcnt/100
    starttime=time.time()
    for line in open(inputpath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        makeset(info[0],info[1])
        solvecnt+=1
        if random.random()*ratecnt<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("subgraphinfo(%s), remain %02d:%02d:%02d"%(inputpath,h,m,s))
    fw=open(outputpath,"w")
    cid=0
    com=dict()
    comsi=dict()
    for u in fa:
        f=find(u)
        if f not in com:
            cid+=1
            com[f]=cid
        i=com[f]
        fw.write("%d,%d\n"%(u,i))
        comsi[i]=1 if i not in comsi else comsi[i]+1
    fw.close()
    fw=open(comsizepath,"w")
    cd=-1
    for c in sorted(comsi.items(),key=lambda arg:arg[1]):
        fw.write("%d,%d\n"%(c[0],c[1]))
        cd=c[0]
    fw.close()
    return cd
def loadmaxcpuser(userbelongpath,compomentid):
    global ub
    ub=set()
    for line in open(userbelongpath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        if compomentid==info[1]:ub.add(info[0])
def getsubgraph(networkpath,maxcompomentpath):
    fw=open(maxcompomentpath,"w")
    solvecnt=0
    totalcnt=countline(networkpath)
    ratecnt=totalcnt/100
    starttime=time.time()
    for line in open(networkpath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        if info[0] in ub and info[1] in ub:fw.write(line)
        solvecnt+=1
        if random.random()*ratecnt<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("getsubgraph(%s), remain %02d:%02d:%02d"%(networkpath,h,m,s))
    fw.close()
if __name__=="__main__":
    for mon in range(201409,201412):
        cd=subgraphinfo("e2014/subnet"+str(mon)+".txt","e2014/user2compoment"+str(mon)+".txt","e2014/compomentsize"+str(mon)+".txt")
        loadmaxcpuser("e2014/user2compoment"+str(mon)+".txt",cd)
        getsubgraph("e2014/subnet"+str(mon)+".txt","e2014/maxcpsocialnet"+str(mon)+".txt")
        getsubgraph("e2014/distnet"+str(mon)+".txt","e2014/maxcpdistnet"+str(mon)+".txt")
        getsubgraph("e2014/gravnet"+str(mon)+".txt","e2014/maxcpgravnet"+str(mon)+".txt")
