package train

import org.apache.spark.sql.SparkSession
import org.apache.spark.{SparkConf, SparkContext}

object T1 {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
    conf.setAppName("CalUserBitmapIndex").setMaster("local")
    val sc = new SparkContext(conf)
    val spark = SparkSession.builder().config(conf).getOrCreate()
    val df = spark
      .createDataFrame(
        Seq(
          (1, 2, 3),
          (4, 5, 6),
          (41, 51, 61)
        )
      )
      .toDF("id", "age", "imsi")
    df.createOrReplaceTempView("d")
    spark.sql("select * from d where id>4").show()

    //    val rdd=sc.parallelize(Array(1,2,3,4,5,6),3)
    //    val r=rdd.mapPartitionsWithIndex((i,xs)=>{
    //      val buffer=ListBuffer[(Int,Int)]()
    //      for(x<-xs){
    //        buffer.append((i,x))
    //      }
    //      buffer.iterator
    //    }).aggregateByKey("$")((x,y)=>{
    //      x + "|" + y
    //    }, (x, y) => {
    //      x + "|" + y
    //    }).collect().foreach(println)

  }
}
