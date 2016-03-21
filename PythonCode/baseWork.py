import math
import os
import time
import random
def mergedata(paths,outputpath):
    base=dict()
    cnt=0
    for path in paths:
        for line in open(path,"r"):
            info=line.strip().split(",")
            if(info[0].find("-")!=-1):ba=info[0]
            else:
                ba=int(info[0])
                ba=str(ba//100000)+"-"+str(ba%100000)
            loc="%.6f,%.6f"%(float(info[1]),float(info[2]))
            if ba not in base:base[ba]=loc
            else:
                cnt+=1
                print("%04d-->%s\t%s\t%s"%(cnt,ba,base[ba],loc))
    fw=open(outputpath,"w")
    for x in sorted(base.items(),key=lambda arg:arg[0]):
        fw.write("%s,%s\n"%(x[0],x[1]))
    fw.close()
def extractbase(inputpath,outputpath):
    #base,x,y,planeNo,planeAttr,planeName,planeContain,planeID,planeArea
    fw=open(outputpath,"w")
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        #print(info)
        try:
            fw.write("%s,%s,%s,%s,%s,%s\n"%(info[0],info[1],info[2],info[-2],info[-1][:info[-1].index(".")] if info[-1].find(".")!=-1 else info[-1],info[4]))
        except:
            print(line)
            os._exit(-1)
    fw.close()
def getplane(inputpath,outputpath):
    fw=open(outputpath,"w")
    ba=dict()
    for line in open(inputpath,"r"):
        if line.find("plane")!=-1:continue
        info=line.strip().split(",")
        x=float(info[1])
        y=float(info[2])
        if info[3] not in ba:
            ba[info[3]]=[x,y,1]
        else:
            ba[info[3]][0]+=x
            ba[info[3]][1]+=y
            ba[info[3]][2]+=1
    for x in sorted(ba.items(),key=lambda arg:int(arg[0])):
        fw.write("%s,%.6f,%.6f\n"%(x[0],x[1][0]/x[1][2],x[1][1]/x[1][2]))
    fw.close()
def toangle(d):
    return d*math.pi/180.0
def dist(x1,y1,x2,y2):
    if x1==x2 and y1==y2:return 0
    x1=toangle(x1)
    y1=toangle(y1)
    x2=toangle(x2)
    y2=toangle(y2)
    s=math.cos(y1)*math.cos(y2)*math.cos(x1-x2)+math.sin(y1)*math.sin(y2)
    return 6370*math.acos(s)
def getoddistance(inputpath,outputpath):
    point=list()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        point.append([int(info[0]),float(info[1]),float(info[2])])
    fw=open(outputpath,"w")
    di=list()
    for a in point:
        fw.write(str(a[0]))
        for b in point:
            d=dist(a[1],a[2],b[1],b[2])
            if d!=0:
                di.append(d)
            fw.write(",%.6f"%(d))
        fw.write("\n")
    fw.close()
    m=1.0/len(di)
    ave=1
    for d in di:ave*=math.pow(d,m)
    print("ave->%.6f"%(ave))
if __name__=="__main__":
    #extractbase("BasePlane.csv","BasePlaneSimple.csv")
    #getplane("BasePlaneSimple.csv","PlaneInfo.txt")
    getoddistance("PlaneInfo.txt","DistanceOD.txt")
