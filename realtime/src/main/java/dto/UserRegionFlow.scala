package dto

case class UserRegionFlow( //1:流入，0，表示流出
    isIn: Int,
    regionId: String,
    gender: Int,
    age: Int
)
