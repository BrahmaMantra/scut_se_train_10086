package train

import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.mutable.ListBuffer

object MapTest {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
    conf.setAppName("CalUserBitmapIndex").setMaster("local")
    val sc = new SparkContext(conf)
    val rdd = sc.parallelize(Array(1, 2, 3, 4, 5, 6), 3)
    rdd
      .mapPartitionsWithIndex((i, xs) => {
        val ar = ListBuffer[(Int, Int)]()
        for (x <- xs) {
          ar.append((i, x + 1))
        }
        ar.iterator
      })
      .repartition(4)
      .aggregateByKey(")")(
        (x, y) => {
          x + "=" + y
        },
        (x, y) => {
          x + "+" + y
        }
      )
      .collect()
      .foreach(println)

  }
}
