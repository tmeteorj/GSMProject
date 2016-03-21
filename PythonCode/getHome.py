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
    return hour,minu,secs
def memUsed():
    m=psutil.virtual_memory()
    return m.percent,m.used,m.total
def countline(filePath):
    count=0
    f=open(filePath,"rb")
    sol=0
    totalSize=os.path.getsize(filePath)/1024/1024/1024
    while True:
        buff=f.read(1024*1024*1024)
        if not buff:break
        sol+=1
        print("countline(%s) %dG"%(filePath,sol))
        count+=buff.count("\n")
        if(sol==2):
            count=count/2.0*totalSize
            break
    f.close()
    return count
def statisticalPeopleHour(inputpath,allhourpath,nighthourpath):
    allh=dict()
    nighth=dict()
    solvecnt=0
    totalcnt=countline(inputpath)
    starttime=time.time()
    for line in open(inputpath,"r"):
        #id,all,night
        info=[int(t) for t in line.strip().split(",")]
        allh[info[1]]=1 if info[1] not in allh else allh[info[1]]+1
        nighth[info[2]]=1 if info[2] not in nighth else nighth[info[2]]+1
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("statisticalPeopleHour(%s,%s,%s): solve %d, total %d, completed %.3f%%, remain %02d:%02d:%02d"%(inputpath,allhourpath,nighthourpath,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    fw_a=open(allhourpath,"w")
    fw_a.write("staytime,count,acccount\n")
    tot=0
    for x in sorted(allh.items(),key=lambda arg:arg[0]):
        tot+=x[1]
        fw_a.write("%d,%d,%d\n"%(x[0],x[1],tot))
    fw_a.close()
    fw_b=open(nighthourpath,"w")
    fw_b.write("staytime,count,acccount\n")
    tot=0
    for x in sorted(nighth.items(),key=lambda arg:arg[0]):
        tot+=x[1]
        fw_b.write("%d,%d,%d\n"%(x[0],x[1],tot))
    fw_b.close()
def extractUserpath(staypath,userpath,thred):
    fw=open(userpath,"w")
    for line in open(staypath,"r"):
        if line.find("count")!=-1:continue
        info=[int(t) for t in line.strip().split(",")]
        if info[2]>=thred:
            fw.write(str(info[0])+"\n")
    fw.close()
def gethome(trajpath,userpath,homepath):
    global base
    solvecnt=0
    totalcnt=countline(userpath)
    starttime=time.time()
    user=dict()
    for line in open(userpath,"r"):
        user[line.strip()]=dict()
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("loaduserpath(%s): solve %d, total %d, completed %.3f%%, remain %02d:%02d:%02d"%(userpath,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    solvecnt=0
    totalcnt=countline(trajpath)
    starttime=time.time()
    for line in open(trajpath,"r"):
        #time,loc,id
        info=line.strip().split(",")
        if info[2] in user:
            #20140909 10:10:10
            hr=int(info[0][9:11])
            if (hr>=21 or hr<7) and info[1] in base:
                plane=base[info[1]]
                user[info[2]][plane]=1 if plane not in user[info[2]] else user[info[2]][plane]+1
        solvecnt+=1
        if random.random()*1000000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("worktrajpath(%s): solve %d, total %d, completed %.3f%%, remain %02d:%02d:%02d"%(trajpath,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    solvecnt=0
    totalcnt=len(user)
    starttime=time.time()
    fw=open(homepath,"w")
    for u in user:
        maxcnt=0
        maxloc="null"
        for x in user[u]:
            if user[u][x]>maxcnt:
                maxcnt=user[u][x]
                maxloc=x
        fw.write("%s,%s\n"%(u,maxloc))
        solvecnt+=1
        if random.random()*100000<1:
            h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
            print("gethome(): solve %d, total %d, completed %.3f%%, remain %02d:%02d:%02d"%(solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    fw.close()
def loadexistbase(filePath):
    global base
    base=dict()
    for line in open(filePath,"r"):
        info=line.strip().split(",")
        base[info[0]]=info[3]
def blockbelong(inputpath,outputpath):
    global base
    fw=open(outputpath,"w")
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        if info[1] in base:fw.write("%s,%s\n"%(info[0],base[info[1]]))
        else:fw.write("%s,null\n"%(info[0]))
    fw.close()
if __name__=="__main__":
    if not os.path.exists("home2014"):os.mkdir("home2014")
    loadexistbase("BasePlaneSimple.csv")
    for month in range(201409,201412):
    #statisticalPeopleHour("PeopleStayTime/user_201409.txt","PeopleStayTime/all_201409.txt","PeopleStayTime/night_201409.txt")
        #extractUserpath("PeopleStayTime/user_"+str(month)+".txt","PeopleStayTime/tjuser_"+str(month)+".txt",110)
        #gethome("traj2014/r"+str(month)+".txt","PeopleStayTime/tjuser_"+str(month)+".txt","home2014/bhome"+str(month)+".txt")
        blockbelong("home2014/bhome"+str(month)+".txt","home2014/phome"+str(month)+".txt")


