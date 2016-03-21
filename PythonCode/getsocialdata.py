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
def getsocial(inputpath,outputpath):
    totalcnt=countline(inputpath)
    solvecnt=0
    rate=max(totalcnt/10000,1)
    starttime=time.time()
    fw=open(outputpath,"w")
    for line in open(inputpath,"r"):
        if(line[0]=="#"):continue
        info=line.split(" ")
        social=info[0].split(":")
        user=info[2][1:-1]
        idx=min(len(social)-1,1)
        fw.write("%s,%s\n"%(user,social[idx]))
        solvecnt+=1
        if(random.random()*rate<1):
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("[%s] solve %d, total %d, completed %.4f%%, remain time %02d:%02d:%02d"%("getsocial",solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    fw.close()
if __name__=="__main__":
    for mon in range(201409,201412):
        getsocial("e2014/maxcpsocialinfonet"+str(mon)+".tree","e2014/maxcpsocialnode"+str(mon)+".txt")
        getsocial("e2014/maxcpdistinfonet"+str(mon)+".tree","e2014/maxcpdistsocialnode"+str(mon)+".txt")
        getsocial("e2014/maxcpgravinfonet"+str(mon)+".tree","e2014/maxcpgravsocialnode"+str(mon)+".txt")

