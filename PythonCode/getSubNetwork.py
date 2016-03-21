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
def mergeNetwork(inputpath,outputdir):
    fw=dict()
    lastuser="null"
    lastmonth="null"
    lastcall=0
    solvecnt=0
    totalcnt=countline(inputpath)
    starttime=time.time()
    for x in open(inputpath,"r"):
        #a,b,time\tcall,mess
        y=x.strip().split("\t")
        u=y[0].split(",")
        n=y[1].split(",")
        nowuser=u[0]+","+u[1]
        nowmonth=u[2][0:6]
        if nowuser!=lastuser:
            if lastuser!="null":
                if lastmonth not in fw:fw[lastmonth]=open(outputdir+"/net"+lastmonth+".txt","w")
                if lastcall>0:fw[lastmonth].write("%s,%d\n"%(lastuser,lastcall))
                lastcall=0
        elif nowmonth!=lastmonth:
            if lastmonth not in fw:fw[lastmonth]=open(outputdir+"/net"+lastmonth+".txt","w")
            if lastcall>0:fw[lastmonth].write("%s,%d\n"%(lastuser,lastcall))
            lastcall=0
        lastuser=nowuser
        lastmonth=nowmonth
        lastcall+=int(n[0])
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("mergeNetwork(%s): solve %d, total %d, completed %.3f%%, remain %02d:%02d:%02d"%(inputpath,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    if lastuser!="null":
        if lastmonth not in fw:fw[lastmonth]=open(outputdir+"/net"+lastmonth+".txt","w")
        if lastcall>0:fw[lastmonth].write("%s,%d\n"%(lastuser,lastcall))
    for month in fw:fw[month].close()   
def getSubnetwork(inputpath,userpath,outputpath):
    user=set()
    for x in open(userpath,"r"):
        if x.find("null")!=-1:continue
        y=x.strip().split(",")
        user.add(y[0])
    fw=open(outputpath,"w")
    solvecnt=0
    totalcnt=countline(inputpath)
    starttime=time.time()
    for x in open(inputpath,"r"):
        #a,b,call
        y=x.strip().split(",")
        if y[0] in user and y[1] in user:
            fw.write(x)
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("getSubnetwork(%s): solve %d, total %d, completed %.3f%%, remain %02d:%02d:%02d"%(inputpath,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    fw.close()
if __name__=="__main__":
    mergeNetwork("e2014/network.txt","e2014")
    for month in range(201409,201412):
        getSubnetwork("e2014/net"+str(month)+".txt","home2014/bhome"+str(month)+".txt","e2014/subnet"+str(month)+".txt")
