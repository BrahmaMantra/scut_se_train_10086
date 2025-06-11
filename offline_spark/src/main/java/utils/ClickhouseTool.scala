package utils

import com.clickhouse.jdbc.ClickHouseDataSource
import ru.yandex.clickhouse.settings.ClickHouseQueryParam

import java.util.Properties

object ClickhouseTool {
  def getConn()={
    val url = "jdbc:clickhouse://bigdata01:8123"
    val prop = new Properties()
    prop.setProperty(ClickHouseQueryParam.USER.getKey, "default")
    prop.setProperty(ClickHouseQueryParam.PASSWORD.getKey, "clickhouse")
    val dataSource = new ClickHouseDataSource(url, prop)
    val conn = dataSource.getConnection
    conn
  }

}
