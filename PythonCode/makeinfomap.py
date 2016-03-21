import time
import random
import os
import psutil
def timeEvaluation(solvecnt,totalcnt,costtime):
    totalcnt=max(totalcnt,solvecnt)
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
def getinfodata(inputpath,outputpath):
    #u1,u2,call
    totalcnt=countline(inputpath)
    rate=max(totalcnt/10000,1)
    solvecnt=0
    starttime=time.time()
    hsc=dict()
    ic=0
    tmpc=open("tmpcall","w")
    ice=0
    for line in open(inputpath,"r"):
        item=line.strip().split(",")
        if item[2]!="0":
            u=list()
            for i in range(2):
                if item[i] in hsc:u.append(hsc[item[i]])
                else:
                    ic+=1
                    hsc[item[i]]=ic
                    u.append(ic)
            ice+=1
            tmpc.write("%d %d %s\n"%(u[0],u[1],item[2]))
        solvecnt+=1
        if random.random()*rate<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("[%s] solve %d, total %d, completed %.4f%%, remain %02d:%02d:%02d"%("getinfodata",solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    tmpc.close()
    fwc=open(outputpath,"w")
    fwc.write("*Vertices %d\n"%(ic))
    for x in sorted(hsc.items(),key=lambda arg:arg[1]):
        fwc.write("%d \"%s\"\n"%(x[1],x[0]))
    fwc.write("*Edges %d\n"%(ice))
    for line in open("tmpcall","r"):
        fwc.write(line)
    fwc.close()
    os.remove("tmpcall")    
if __name__=="__main__":
    for mon in range(201409,201412):
        getinfodata("e2014/maxcpsocialnet"+str(mon)+".txt","e2014/maxcpsocialinfonet"+str(mon)+".net")
        getinfodata("e2014/maxcpdistnet"+str(mon)+".txt","e2014/maxcpdistinfonet"+str(mon)+".net")
        getinfodata("e2014/maxcpgravnet"+str(mon)+".txt","e2014/maxcpgravinfonet"+str(mon)+".net")
