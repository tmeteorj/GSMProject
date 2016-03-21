package Decision.Tree;

import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

import Decision.Tree.Data.Record;

public abstract class DecisionTree {
	protected static String attr[]={"地块面积","人口数量","人口密度","原通讯网络社团个数","限于距离影响的通讯网络社团个数",
		"限于引力影响的通讯网络社团个数","原通讯网络社团密度","限于距离影响的通讯网络社团密度","限于引力影响的通讯网络社团密度",
		"通讯网络社团结果与限于距离影响的社团结果的NMI值","通讯网络社团结果与限于引力影响的社团结果的NMI值","通讯网络社团结果与地块划分结果的NMI值",
		"限于距离影响的社团结果与限于引力影响的社团结果的NMI值","限于距离影响的社团结果与地块划分结果的NMI值","限于引力影响的社团结果与地块划分结果的NMI值"};
	
	
	protected double info;
	protected Record record[];
	protected int splitIndex;
	protected double splitVal;
	protected int label,leftlabel,rightlabel;
	protected HashMap<String,Integer> typeCnt;
	protected DecisionTree leftchild,rightchild;
	public DecisionTree(){
		leftchild=null;
		rightchild=null;
	}
	public int getSize(){
		return record.length;
	}
	public void loadRecord(Record []rf,int left,int right){
		int len=right-left;
		record=new Record[len];
		for(int i=0;i<len;i++){
			record[i]=rf[left+i];
		}
	}
	public void addTypeOne(HashMap<String,Integer> hash,String type){
		int cnt=1;
		if(hash.containsKey(type)){
			cnt+=hash.get(type);
		}
		hash.put(type, cnt);
	}
	
	public String getSubTreeType(){
		int maxcnt=-1;
		String type=null;
		for(Iterator it=typeCnt.entrySet().iterator();it.hasNext();){
			Map.Entry<String, Integer> entry=(Entry<String, Integer>) it.next();
			if(maxcnt<entry.getValue()){
				maxcnt=entry.getValue();
				type=entry.getKey();
			}
		}
		return type;
	}
	public String findClass(Record r){
		if(leftchild==null||rightchild==null){
			return getSubTreeType();
		}else if(r.getAttr(splitIndex)<splitVal){
			return leftchild.findClass(r);
		}else{
			return rightchild.findClass(r);
		}
	}
	
	abstract public void computeInfo();
	abstract public boolean buildTree(int attrsize);
	
}
