package dto

case class RegionCal(
    regionId: String,
    var age_10_20: Int,
    var age_20_40: Int,
    var age_40: Int,
    var manNum: Int,
    var womanNum: Int
)
