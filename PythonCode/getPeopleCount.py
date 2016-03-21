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
def peopleCount(userpath,outputpath):
    pc=dict()
    for line in open("PlaneInfo.txt","r"):
        info=line.strip().split(",")
        pc[info[0]]=0
    for line in open(userpath,"r"):
        if line.find("null")!=-1:continue
        info=line.strip().split(",")
        #user,planeid
        pc[info[1]]=1 if info[1] not in pc else pc[info[1]]+1
    fw=open(outputpath,"w")
    for p in sorted(pc.items(),key=lambda arg:int(arg[0])):
        fw.write("%s,%d\n"%(p[0],p[1]))
    fw.close()
if __name__=="__main__":
    for mon in range(201409,201412):
        peopleCount("home2014/phome"+str(mon)+".txt","home2014/pcount"+str(mon)+".txt")

