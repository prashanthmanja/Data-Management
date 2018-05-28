import java.io.IOException;
import java.util.Iterator;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class Prashanth_Manja_Average {

  public static class TokenizerMapper
       extends Mapper<Object, Text, Text, Text>{


    Text textKey = new Text();
	Text textValue = new Text();
	//Mapper class	
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
			String[] fields = (value.toString().split("\n"));
                        for(String field :fields ) {
                        
                                //field=field.replaceAll("{}","");
                                field=field.replaceAll("[\\[\\](){}]","");
				field=field.replace("\"","");
				String[] b=field.split(",");
                                
                                int age= Integer.parseInt(b[4].split(":")[1]);
                                String balance=b[1].split(":")[1];
				String state=b[10].split(":")[1];
                                
                                if (age>=20 && age<=30){
				textKey.set(state);
				textValue.set(balance);
                                context.write(textKey,textValue);
                                }
                            
                        
    }

    }
	   }
//Combiner class
 public static class IntSumCombiner
       extends Reducer<Text,Text,Text,Text> {
    Text result = new Text();
	

    public void reduce(Text key, Iterable<Text> values,
                       Context context
                       ) throws IOException, InterruptedException {
    
 Integer count = 0;
   Double sum = 0D;
  Iterator<Text> itr = values.iterator();
   while (itr.hasNext()) {
    final String text = itr.next().toString();
    final Double value = Double.parseDouble(text);
    count++;
    sum += value;
   }
        //result.set(sum,count);
        //context.write(key, result);
	context.write(key, new Text(sum+"_"+count));
    }
  }

//Reducer class
  public static class IntSumReducer
       extends Reducer<Text,Text,Text,Text> {
    private Text result = new Text();

    public void reduce(Text key,Iterable<Text> values,
                       Context context
                       ) throws IOException, InterruptedException {
   Double totalsum = 0D;
   Integer totalcount = 0;
   Iterator<Text> itr = values.iterator();
   while (itr.hasNext()) {
    final String text = itr.next().toString();
    final String[] tokens = text.split("_");
    final Double sum = Double.parseDouble(tokens[0]);
    final Integer count = Integer.parseInt(tokens[1]);
    totalsum += sum;
    totalcount += count;
   }




        Double average = totalsum/totalcount;
	//System.out.println("Completed Step one"+average);
	context.write(key,new Text(average.toString()));

    }
  }

 public static void main(String [] args) throws Exception{
        Configuration conf = new Configuration();
        String [] otherArgs = new GenericOptionsParser(conf,args).getRemainingArgs();
        if(otherArgs.length < 2){
                System.err.println("AvgBalance");
                System.exit(2);
        }
        Job job = Job.getInstance(conf,"average balance");
        job.setJarByClass(Prashanth_Manja_Average.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumCombiner.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
	
	//Log log = LogFactory.getLog(MyReducer.class);
	
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0:1);
        System.exit(job.waitForCompletion(true) ? 0:1);

}}
