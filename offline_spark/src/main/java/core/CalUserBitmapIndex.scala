package core

import com.clickhouse.jdbc.ClickHouseDataSource
import org.apache.spark.{SparkConf, SparkContext}
import ru.yandex.clickhouse.settings.ClickHouseQueryParam
import utils.ClickhouseTool

import java.util.Properties

/**
 * 要给每个用户生成唯一id： zipWithUniqueID   :   imsi -- id
 */
object CalUserBitmapIndex {
  def main(args: Array[String]): Unit = {
    val conf=new SparkConf()
    conf.setAppName("CalUserBitmapIndex").setMaster("local")
    val sc=new SparkContext(conf)

    val imsiId=sc.textFile("hdfs://bigdata01:9000/data/userInfo").map(line=>{
      val arr=line.split("\\|")
      val imsi=arr(0)
      imsi
    }).zipWithUniqueId()
//      .collect().foreach(println)
      .foreachPartition(it=>{
      val conn=ClickhouseTool.getConn()
      val stmt=conn.createStatement()
      it.foreach(tup=>{
        val imsi=tup._1
        val id=tup._2
        stmt.executeUpdate(s"insert into USER_INDEX(IMSI,BITMAP_ID) VALUES('${imsi}','${id}')")
      })
      conn.close()

    })

    sc.stop()


  }

}
