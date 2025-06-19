package utils

import com.clickhouse.jdbc.{ClickHouseConnection, ClickHouseDataSource}
import org.apache.spark.sql.{DataFrame, SparkSession}
import ru.yandex.clickhouse.settings.ClickHouseQueryParam

import java.util.Properties

object ClickhouseTool {
  def getConn: ClickHouseConnection = {
    val url = "jdbc:clickhouse://bigdata01:8123"
    val prop = new Properties()
    prop.setProperty(ClickHouseQueryParam.USER.getKey, "default")
    prop.setProperty(ClickHouseQueryParam.PASSWORD.getKey, "clickhouse")
    val dataSource = new ClickHouseDataSource(url, prop)
    val conn = dataSource.getConnection
    conn
  }

  def getUserBitmapIndex(sparkSession: SparkSession): DataFrame = {
    val url = "jdbc:clickhouse://bigdata01:8123"
    val prop = new Properties()
    prop.setProperty("driver", "com.clickhouse.jdbc.ClickHouseDriver")
    prop.setProperty("user", "default")
    prop.setProperty("password", "clickhouse")
    sparkSession.read.jdbc(url, "USER_INDEX", prop)
  }

}
