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
def distrcount(inputpath,outputpath,title,col):
    fw=open(outputpath,"w")
    fw.write("%s,P\n"%(title))
    dc=dict()
    tot=0
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        dc[info[col]]=1 if info[col] not in dc else dc[info[col]]+1
        tot+=1
    for x in dc:
        fw.write("%s,%.8f\n"%(x,dc[x]*1.0/tot))
    fw.close()
def distrcountcluster(inputpath,outputpath,title,col,internum=100):
    fw=open(outputpath,"w")
    fw.write("%s,P\n"%(title))
    dc=dict()
    li=list()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        li.append(float(info[1]))
    tot=len(li)
    li.sort()
    left=min(li)
    right=max(li)
    ave=(right-left)*1.0/internum
    now=left
    cnt=0
    for x in li:
        if x<now+ave:
            cnt+=1
#            print("%f->%d\n"%(x,cnt))
        else:
            dc[now+ave/2.0]=cnt
            now+=ave
            while now+ave<=x:
                dc[now+ave/2.0]=0
                now+=ave
            cnt=1
    dc[now+ave/2.0]=cnt
    for x in dc:
        fw.write("%.4f,%.10f\n"%(x,dc[x]*1.0/tot))
    fw.close()
if __name__=="__main__":
    distrcountcluster("result/pcount201409.txt","result/pcountdistr.csv","PlanePeople",1,100)
    distrcountcluster("result/planedistnode201409.txt","result/planedistnodedistr.csv","PlaneDistCom",1,100)
    distrcountcluster("result/planegravnode201409.txt","result/planegravnodedistr.csv","PlaneGravCom",1,100)
    distrcountcluster("result/planesocialnode201409.txt","result/planesocialnodedistr.csv","PlaneSocialCom",1,100)


