package core

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.{IntegerType, StringType, StructType}
import utils.BitmapUtils
import utils.ClickhouseTool

import scala.collection.mutable

/** 1  1  bitmap 男性
  * 2  0  bitmap 女性
  * 3  10 bitmap  10——20岁
  * 4  20 bitmap  20-40岁
  * 5  40 bitmap  40岁以上
  *
  * 拿到 user bitmap index
  * 确认每一类属性的用户位图
  * 1 、 sql : :类型id，用户id arr
  * 2、 用户id arr --> 用户位图
  *
  * 输出到ck
  */
object CalUserPersonBitmap {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local")
    val sparkSession = SparkSession
      .builder()
      .appName("CalUserPersonBitmap")
      .config(conf)
      .getOrCreate()

    val userInfoStruct = new StructType()
      .add("imsi", StringType)
      .add("gender", StringType)
      .add("age", IntegerType)

    val userInfoDf = sparkSession.read
      .format("csv")
      .option("sep", "|")
      .schema(userInfoStruct)
      .load("hdfs://bigdata01:9000/data/userInfo")

    userInfoDf.createOrReplaceTempView("user_info")

    val userBitmapIndex = ClickhouseTool.getUserBitmapIndex(sparkSession)
    userBitmapIndex.createOrReplaceTempView("user_index")

    val sql =
      """
        | with tmp_res as (
        | select ui.BITMAP_ID,gender,age_flag
        | from (
        | select imsi ,gender,
        | case
        |   when (age>=10 and age<20) then '10'
        |   when (age>=20 and age<40) then '20'
        |   when (age>=40) then '40'
        | end as age_flag
        |
        | from user_info
        | where age>=10
        |  ) as tmp join user_index as ui
        |  on tmp.imsi=ui.IMSI
        |  )
        |
        |
        |select
        |  case
        |  when gender=='1' then 1
        |  when gender=='0' then 2
        |  end as PORTRAIT_ID,
        |  gender as PORTRAIT_VALUE,
        |  case
        |    when gender=='1' then '男性'
        |    when gender=='0' then '女性'
        |    end as COMMENT,
        |  collect_set(BITMAP_ID)  as bitmapIds
        |from
        |tmp_res group by gender
        |
        |union
        |select
        |case
        |when age_flag=='10' then 3
        |when age_flag=='20' then 4
        |when age_flag=='40' then 5
        |end as PORTRAIT_ID,
        |age_flag as PORTRAIT_VALUE,
        |case
        |when age_flag=='10' then '10——20岁'
        |when age_flag=='20' then '20-40岁'
        |when age_flag=='40' then '40岁以上'
        |end as COMMENT,
        | collect_set(BITMAP_ID)  as bitmapIds
        |
        |from tmp_res group by age_flag
        |""".stripMargin

    sparkSession
      .sql(sql)
      .rdd
      .foreachPartition(it => {
        val conn = ClickhouseTool.getConn
        it.foreach(row => {
          val id = row.getAs[Int]("PORTRAIT_ID")
          val value = row.getAs[String]("PORTRAIT_VALUE")
          val comment = row.getAs[String]("COMMENT")
          val bitArr =
            row.getAs[mutable.WrappedArray[java.math.BigDecimal]]("bitmapIds")
          val ckBitmap = BitmapUtils.bitmapIdsToClickHouseBitmap(bitArr)
          val stmt = conn.prepareStatement(
            s"insert into TA_PORTRAIT_IMSI_BITMAP " +
              s"(PORTRAIT_ID,PORTRAIT_VALUE,PORTRAIT_BITMAP,COMMENT) values (?,?,?,?)"
          )
          stmt.setInt(1, id)
          stmt.setString(2, value)
          stmt.setObject(3, ckBitmap)
          stmt.setString(4, comment)
          stmt.executeUpdate()
          stmt.close()

        })
        conn.close()
      })
    sparkSession.stop()

  }

}
