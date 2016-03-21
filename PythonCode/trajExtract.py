import time
import random
import os
import gzip
import psutil
def timeEvaluation(solvecnt,totalcnt,costtime):
    avetime=costtime*1.0/solvecnt
    remaintime=avetime*(totalcnt-solvecnt)
    hour=remaintime//3600
    minu=remaintime%3600/60
    secs=int(remaintime%60)
    return hour,minu,secs
def memUsed():
    m=psutil.virtual_memory()
    return m.percent,m.used,m.total
def countline(filePath):
    count=0
    f=open(filePath,"rb")
    while True:
        buff=f.read(8192*1024)
        if not buff:break
        count+=buff.count("\n")
    f.close()
    return count
def loadbaseinfo(base2d,base3d):
    global base
    base=dict()
    for line in open(base2d,"r"):
        ba=line[:line.index(",")]
        xy=line[line.index(","):].strip()
        big=int(ba)//100000
        small=int(ba)%100000
        base[str(big)+"-"+str(small)]=xy
    for line in open(base3d,"r"):
        ba=line[:line.index(",")]
        xy=line[line.index(","):].strip()
        big=int(ba)//100000
        small=int(ba)%100000
        base[str(big)+"-"+str(small)]=xy
def gettrajrecord(inputdirs,outputdir):
    global base
    totalcnt=0
    solvecnt=0
    for inputdir in inputdirs:
        totalcnt+=len(os.listdir(inputdir))
    starttime=time.time()
    fw=dict()
    for inputdir in inputdirs:
        files=os.listdir(inputdir)
        files.sort()
        for f in files:
            for line in gzip.open(inputdir+"/"+f,"rb"):
                info=line.decode("utf-8").strip().split(",")
                hr=int(info[1][9:11]])
                if info[0]!="13":continue
                if hr>7 and hr<21:continue
                ba=info[2]+"-"+info[3]
                if ba not in base:continue
                name=info[1][0:8]
                if name not in fw:fw[name]=open(outputdir+"/"+name+".txt","w")
                fw[name].write("%s,%s,%s,%s\n"%(info[0],info[1][0:17],ba,info[4])
            solvecnt+=1
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("gettrajrecord[%s] solvecnt: %d, totalcnt: %d, completed: %.3f%%, remain %02d:%02d:%02d\n"%(inputdir,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    for name in fw:fw[name].close()
def loaddict(inputpath):
    global hasuser
    hasuser=dict()
    for x in open(inputpath,"r"):
        y=x.strip().split(",")
        hasuser[y[0]]=y[1]
def indextrajrecord(intputdir,outputdir):
    global hasuser
    files=os.listdir(inputdir)
    files.sort()
    solvecnt=0
    totalcnt=len(files)
    starttime=time.time()
    nowmon=201408
    for name in files:
        if int(name[0:8])!=nowmon:
            nowmon+=1
            loaddict("hashdir/h"+str(nowmon)+".txt")
        fw=open(outputdir+"/"+name,"w")
        for line in open(inputdir+"/"+name,"r"):
            info=line.strip().split(",")
            if info[-1] in hauser:
                fw.write("%s,%s,%s,%s\n"%(info[0],info[1],info[2],hauser[info[3]]]))
        fw.close()
        solvecnt+=1
        h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
        print("indextrajrecord[%s] solvecnt: %d, totalcnt: %d, completed: %.3f%%, remain %02d:%02d:%02d\n"%(name,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
if __name__=="__main__":
    loadbaseinfo("2G-data.csv","TD-data.csv")
    gettrajrecord(["201409","201410","201411"],"traj2014")
    indextrajrecord("traj2014","traj2014i")
