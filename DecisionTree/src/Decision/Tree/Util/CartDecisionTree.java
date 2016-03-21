package Decision.Tree.Util;

import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;

import Decision.Tree.DecisionTree;
import Decision.Tree.Data.Record;

public class CartDecisionTree extends DecisionTree{
	
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public void computeInfo(){
		info=1;
		typeCnt=new HashMap<String,Integer>();
		int tot=record.length;
		for(int i=0;i<tot;i++){
			addTypeOne(typeCnt, record[i].getType());
		}
		for(Iterator it=typeCnt.entrySet().iterator();it.hasNext();){
			Map.Entry<String, Integer> entry=(Entry<String, Integer>) it.next();
			double p=entry.getValue()*1.0/tot;
			info-=p*p;
		}
	}
	
	@SuppressWarnings("unchecked")
	public boolean buildTree(int attrsize){
		if(typeCnt.size()<=1){
			return true;
		}
		int maxattr=-1;
		int maxid=-1;
		double maxgain=-1000000;
		for(int id=0;id<attrsize;id++){
			final int index=id;
			Arrays.sort(record,new Comparator(){
				@Override
				public int compare(Object o1, Object o2) {
					Record a=(Record) o1;
					Record b=(Record) o2;
					return a.compareTo(b, index);
				}
			});
			HashMap<String,Integer> leftCnt=new HashMap<String,Integer>();
			for(int i=1;i<record.length;i++){
				addTypeOne(leftCnt,record[i-1].getType());
				double leftInfo=1.0;
				double rightInfo=1.0;
				for(Iterator it=typeCnt.entrySet().iterator();it.hasNext();){
					Map.Entry entry=(Entry) it.next();
					String type=(String) entry.getKey();
					int cntl=0,cntr=(int) entry.getValue();
					if(leftCnt.containsKey(type)){
						cntl=leftCnt.get(type);
						cntr-=cntl;
					}
					if(cntl!=0){
						double p=cntl*1.0/i;
						leftInfo-=p*p;
					}
					if(cntr!=0){
						double p=cntr*1.0/(record.length-i);
						rightInfo-=p*p;
					}
				}
				double subInfo=leftInfo*i/record.length+rightInfo*(record.length-i)/record.length;
				double gain=info-subInfo;
				if(maxgain<gain){
					maxgain=gain;
					maxid=i;
					maxattr=id;
				}
			}
		}
		if(maxid==-1){
			System.out.println("What?!");
			System.exit(-1);
			return false;
		}else{
			leftchild=new CartDecisionTree();
			rightchild=new CartDecisionTree();
			final int index=maxattr;
			Arrays.sort(record,new Comparator(){
				public int compare(Object o1, Object o2) {
					Record a=(Record) o1;
					Record b=(Record) o2;
					return a.compareTo(b, index);
				}
			});
			splitIndex=maxattr;
			splitVal=record[maxid].getAttr(maxattr);
			leftchild.loadRecord(record, 0, maxid);
			leftchild.computeInfo();
			boolean flag=true;
			flag=flag&&leftchild.buildTree(attrsize);
			rightchild.loadRecord(record, maxid, record.length);
			rightchild.computeInfo();
			flag=flag&&rightchild.buildTree(attrsize);
			return flag;
		}
	}
}
