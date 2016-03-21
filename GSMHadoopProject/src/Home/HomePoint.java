package Home;

import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.StringTokenizer;
import java.util.Calendar;
import java.util.Date;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.FileSplit;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

public class HomePoint {

	public static class HomeMapper extends MapReduceBase implements
			Mapper<LongWritable, Text, Text, Text> {
		private Text m_key = new Text();
		private Text m_value = new Text();

		public void map(LongWritable key, Text value,
				OutputCollector<Text, Text> output, Reporter reporter)
				throws IOException {
			String line = value.toString();
			String[] info = line.split(",");
			// type,time,big-small,id
			m_key.set(info[3]);
			m_value.set(info[2]);
			output.collect(m_key, m_value);
		}
	}

	public static class HomeReducer extends MapReduceBase implements
			Reducer<Text, Text, Text, Text> {
		
		public void reduce(Text key, Iterator<Text> values,
				OutputCollector<Text, Text> output, Reporter reporter)
				throws IOException {
			HashMap<String,Integer> baseMap=new HashMap<String,Integer>();
			int maxcnt=0;
			String maxbase=null;
			while(values.hasNext()){
				String ba=values.next().toString();
				int cnt=1;
				if(baseMap.containsKey(ba))cnt+=Integer.parseInt(baseMap.get(ba).toString());
				baseMap.put(ba, cnt);
				if(maxcnt<cnt){
					maxcnt=cnt;
					maxbase=ba;
				}
			}
			if(maxbase!=null){
				output.collect(key, new Text(maxbase));
			}
		}
	}

	public static void main(String[] args) throws Exception {

		JobConf conf = new JobConf(HomePoint.class);
		conf.setJobName("HomePoint"); // 设置一个用户定义的job名称
		conf.setOutputKeyClass(Text.class); // 为job的输出数据设置Key类
		conf.setOutputValueClass(Text.class); // 为job输出设置value类
		conf.setMapperClass(HomeMapper.class); // 建边
		conf.setReducerClass(HomeReducer.class); // 为job设置Reduce类
		conf.setInputFormat(TextInputFormat.class); // 为map-reduce任务设置InputFormat实现类
		conf.setOutputFormat(TextOutputFormat.class); // 为map-reduce任务设置OutputFormat实现类
		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));
		JobClient.runJob(conf); // 运行一个job

	}
}