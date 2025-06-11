package dto

case class RegionCell(
                     regionId:String,
                     laccell:String
                     )
object RegionCell{
  def fromStr(record:String):RegionCell={
    val arr=record.split("\\|")
    RegionCell(arr(0),arr(1))
  }
}
