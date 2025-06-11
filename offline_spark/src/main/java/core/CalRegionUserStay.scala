package core

import com.clickhouse.client.ClickHouseDataType
import com.clickhouse.client.data.ClickHouseBitmap
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.{DoubleType, LongType, StringType, StructType}
import org.roaringbitmap.RoaringBitmap
import utils.ClickhouseTool

import java.util.Properties
import scala.collection.mutable

/** 执行频率：天
 */
object CalRegionUserStay {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local")
    val sparkSession = SparkSession
      .builder()
      .appName("CalRegionUserStay")
      .config(conf)
      .getOrCreate()

    val xdrPath = "hdfs://bigdata01:9000/xdr/20230204/*"
    val xdrStruct = new StructType()
      .add("imsi", StringType)
      .add("laccell", StringType)
      .add("lat", DoubleType)
      .add("lot", DoubleType)
      .add("startTime", LongType)
    val xdrDf = sparkSession.read
      .format("csv")
      .option("sep", "|")
      .schema(xdrStruct)
      .load(xdrPath)

    val regionCellPath = "hdfs://bigdata01:9000/data/regionCell"
    val regionCellStruct = new StructType()
      .add("regionId", StringType)
      .add("laccell", StringType)
    val regionCellDf = sparkSession.read
      .format("csv")
      .option("sep", "|")
      .schema(regionCellStruct)
      .load(regionCellPath)

    //加载用户位图索引数据
    val url = "jdbc:clickhouse://bigdata01:8123"
    val prop = new Properties()
    prop.setProperty("user", "default")
    prop.setProperty("password", "clickhouse")

    val userBitmapIndex = sparkSession.read.jdbc(url, "USER_INDEX", prop)

    xdrDf.createOrReplaceTempView("xdr")
    regionCellDf.createOrReplaceTempView("region_cell")
    userBitmapIndex.createOrReplaceTempView("user_index")

    val sql =
      """
        |
        | select
        |  tmp.regionId,
        |  tmp.produce_hour,
        |  collect_set(tmp.BITMAP_ID) as bitmapIds
        |  from
        |
        | (select
        |  b.regionId ,
        |  from_unixtime( a.startTime/1000,'yyyyMMddHH') as produce_hour,
        |  c.BITMAP_ID
        |  from xdr a
        | left join region_cell b on a.laccell=b.laccell
        | left join user_index c on a.imsi=c.IMSI) as tmp
        | group by tmp.regionId,tmp.produce_hour
        |
        |""".stripMargin

    sparkSession
      .sql(sql)
      .rdd
      .foreachPartition(it => {
        val conn = ClickhouseTool.getConn()
        it.foreach(row => {
          val regionId = row.getAs[String]("regionId")
          val produce_hour = row.getAs[String]("produce_hour")
          val bitmap = new RoaringBitmap()
          val bitArr =
            row.getAs[mutable.WrappedArray[java.math.BigDecimal]]("bitmapIds")
          for (x <- bitArr) {
            bitmap.add(x.intValue())
          }
          val ckbitmap =
            ClickHouseBitmap.wrap(bitmap, ClickHouseDataType.UInt32)
          val stmt = conn.prepareStatement(
            s"insert into REGION_ID_IMSI_BITMAP " +
              s"(REGION_ID,PRODUCE_HOUR,IMSI_INDEXES) values (?,?,?)"
          )
          stmt.setString(1, regionId)
          stmt.setString(2, produce_hour)
          stmt.setObject(3, ckbitmap)
          stmt.executeUpdate()
          stmt.close()

        })
        conn.close()
      })
    sparkSession.stop()

  }
}
