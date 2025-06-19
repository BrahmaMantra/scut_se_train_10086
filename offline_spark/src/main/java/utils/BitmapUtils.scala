package utils

import com.clickhouse.client.ClickHouseDataType
import com.clickhouse.client.data.ClickHouseBitmap
import org.roaringbitmap.RoaringBitmap
import scala.collection.mutable

object BitmapUtils {

  /** 将 BigDecimal 数组转为 RoaringBitmap 并封装为 ClickHouseBitmap
    * @param bitArr WrappedArray[java.math.BigDecimal]
    * @return ClickHouseBitmap
    */
  def bitmapIdsToClickHouseBitmap(
      bitArr: mutable.WrappedArray[java.math.BigDecimal]
  ): ClickHouseBitmap = {
    val bitmap = new RoaringBitmap()
    for (x <- bitArr) {
      bitmap.add(x.intValue())
    }
    ClickHouseBitmap.wrap(bitmap, ClickHouseDataType.UInt32)
  }
}
