package Decision.Tree.Data;

public class Record {
	String type;
	double attr[];
	/**
	 * 
	 * @param line: type,attrs
	 */
	public Record(String line){
		String info[]=line.trim().split(",");
		type=info[1];
		attr=new double[info.length-2];
		for(int i=2;i<info.length;i++){
			attr[i-2]=Double.parseDouble(info[i]);
		}	
	}
	public String getType(){
		return type;
	}
	public double getAttr(int index){
		return attr[index];
	}
	public int compareTo(Record next,int index){
		double a=attr[index];
		double b=next.getAttr(index);
		return a<b?-1:(a>b?1:0);
	}
	public int getAttrSize(){
		return attr.length;
	}
}
