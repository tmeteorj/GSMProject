package Decision.Tree.Process;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

import Decision.Tree.DecisionTree;
import Decision.Tree.Data.Record;
import Decision.Tree.Util.CartDecisionTree;
import Decision.Tree.Util.ID3DecisionTree;

public class Main {
	
	public static void main(String[] args) throws IOException {
		String dataset[]={"plane2014/train_set_0.txt","plane2014/train_set_1.txt","plane2014/train_set_2.txt",
				"plane2014/train_set_3.txt","plane2014/train_set_4.txt","plane2014/train_set_5.txt",
				"plane2014/train_set_6.txt","plane2014/train_set_7.txt","plane2014/train_set_8.txt",
				"plane2014/train_set_9.txt"};
		
		CartDecisionTree cartRoot=new CartDecisionTree();
		ID3DecisionTree id3Root=new ID3DecisionTree();

		buildModel(dataset,9,cartRoot);
		testModel(dataset[9],cartRoot);
		
		buildModel(dataset,9,id3Root);
		testModel(dataset[9],id3Root);
	}
	/**
	 * 
	 * @param trainPath: type,attr1,attr2...
	 */
	public static void buildModel(String trainPaths[],int p,DecisionTree root) throws IOException{
		List<Record> rlist=new ArrayList<Record>();
		for(int i=0;i<10;i++){
			if(i==p)continue;
			BufferedReader br=new BufferedReader(new InputStreamReader(new FileInputStream(new File(trainPaths[i])),"utf-8"));
			String line;
			while((line=br.readLine())!=null){
				rlist.add(new Record(line));
			}
		}
		root=new CartDecisionTree();
		Record []record=rlist.toArray(new Record[rlist.size()]);
		root.loadRecord(record, 0, record.length);
		root.computeInfo();
		root.buildTree(record[0].getAttrSize());
	}
	public static void testModel(String testPath,DecisionTree root)throws IOException{
		BufferedReader br=new BufferedReader(new InputStreamReader(new FileInputStream(new File(testPath)),"utf-8"));
		String line;
		int acc=0;
		int tot=0;
		while((line=br.readLine())!=null){
			Record r=new Record(line);
			String cls=root.findClass(r);
			tot++;
			if(cls.equals(r.getType())){
				acc++;
			}
		}
		System.out.printf("testfile: %s, acc: %d, tot: %d, rate: %.4f%%\n",testPath,acc,tot,acc*100.0/tot);
	}

}
