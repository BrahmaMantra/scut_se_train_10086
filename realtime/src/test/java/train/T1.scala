package train

object T1 {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
    conf.setAppName("CalUserBitmapIndex").setMaster("local")
    val sc = new SparkContext(conf)

  }

}
