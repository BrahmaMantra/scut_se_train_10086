package core

import dto.{RegionCal, RegionCell, UserInfo, UserRegionFlow, UserXdr, XDR}
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.api.common.state.{MapStateDescriptor, ValueState, ValueStateDescriptor}
import org.apache.flink.api.java.io.TextInputFormat
import org.apache.flink.configuration.Configuration
import org.apache.flink.connector.hbase.sink.{HBaseMutationConverter, HBaseSinkFunction}
import org.apache.flink.core.fs.Path
import org.apache.flink.streaming.api.functions.KeyedProcessFunction
import org.apache.flink.streaming.api.functions.co.{BroadcastProcessFunction, KeyedBroadcastProcessFunction}
import org.apache.flink.streaming.api.functions.source.FileProcessingMode
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer
import org.apache.flink.util.Collector
import org.apache.hadoop.conf
import org.apache.hadoop.hbase.client.{Mutation, Put}

import java.util.Properties

/**
 * 1、读取kafka 中的信令
 * 2、用户基础数据、基站和区域关系数据
 * 3、信令与用户基础数据做融合，广播
 * 4、用户出入行政区、按用户做keyby-广播-基站和区域关系数据，分析用户对每个行政区流入流出情况，  保留用户上一个行政区-状态
 * 5、按行政区做统计，按行政区keyby,  timeservice, 每一分钟输出一次统计结果。   状态保存行政区的人员构成统计
 * 6、输出hbase,   key:行政区，value，人员构成
 */
object CalRegionUser {
  def main(args: Array[String]): Unit = {
    val env=StreamExecutionEnvironment.getExecutionEnvironment

    import org.apache.flink.api.scala._

    val prop=new Properties()
    prop.setProperty("bootstrap.servers","bigdata01:9092")

    val kafkaConsumer=new FlinkKafkaConsumer[String]("xdr",new SimpleStringSchema(),prop)

    //读取信令数据
    val xdr=env.addSource(kafkaConsumer).map(x=>XDR.fromKafka(x))


    //获取用户基础数据
    val userInfoPath="hdfs://bigdata01:9000/data/userInfo"
    val userInfoStream=env.readFile(new TextInputFormat(new Path(userInfoPath)),userInfoPath,FileProcessingMode.PROCESS_CONTINUOUSLY,1000)
      .map(x=>UserInfo.fromStr(x))



    //获取基站、区域关系数据
    val regionCellPath = "hdfs://bigdata01:9000/data/regionCell"
    val regionCellStream = env.readFile(new TextInputFormat(new Path(regionCellPath)), regionCellPath, FileProcessingMode.PROCESS_CONTINUOUSLY, 1000)
      .map(x => RegionCell.fromStr(x))


    val broadcastUserInfoDes=new MapStateDescriptor[String,UserInfo](
      "broadcastUserInfoDes",
      classOf[String],
      classOf[UserInfo]
    )

    val userXdrStream=xdr.connect(userInfoStream.broadcast(broadcastUserInfoDes)).process(new BroadcastProcessFunction[XDR,UserInfo,UserXdr] {
      override def processElement(in1: XDR, readOnlyContext: BroadcastProcessFunction[XDR, UserInfo, UserXdr]#ReadOnlyContext, collector: Collector[UserXdr]): Unit = {
        val imsi=in1.imsi
        val laccell=in1.laccell
        val broadcastState=readOnlyContext.getBroadcastState(broadcastUserInfoDes)
        val userinfo=broadcastState.get(imsi)
        if(userinfo!=null){
          val gender=userinfo.gender
          val age=userinfo.age
          collector.collect(UserXdr(imsi, laccell, gender, age))
        }

      }

      override def processBroadcastElement(in2: UserInfo, context: BroadcastProcessFunction[XDR, UserInfo, UserXdr]#Context, collector: Collector[UserXdr]): Unit = {
        val broadcastState=context.getBroadcastState(broadcastUserInfoDes)
        broadcastState.put(in2.imsi,in2)
      }
    })


    //用户出入行政区、按用户做keyby-广播-基站和区域关系数据，分析用户对每个行政区流入流出情况，  保留用户上一个行政区-状态

    val broadcastRegionCellDes = new MapStateDescriptor[String, String](
      "broadcastRegionCellDes",
      classOf[String],//laccell
      classOf[String] //regionId
    )

    val userRegionFlowStream=userXdrStream.keyBy(_.imsi).connect(regionCellStream.broadcast(broadcastRegionCellDes))
      .process(new KeyedBroadcastProcessFunction[String,UserXdr,RegionCell,UserRegionFlow] {
        var lastRegion:ValueState[String]=_

        override def open(parameters: Configuration): Unit = {
          super.open(parameters)
          val lastRegionDes=new ValueStateDescriptor[String](
            "lastRegion",createTypeInformation[String]
          )
          lastRegion=getRuntimeContext.getState(lastRegionDes)
        }
        override def processElement(in1: UserXdr, readOnlyContext: KeyedBroadcastProcessFunction[String, UserXdr, RegionCell, UserRegionFlow]#ReadOnlyContext, collector: Collector[UserRegionFlow]): Unit = {
          val laccell=in1.laccell
          val gender=in1.gender
          val age=in1.age

          val broadcastState = readOnlyContext.getBroadcastState(broadcastRegionCellDes)
          val regionId=Option(broadcastState.get(laccell)).getOrElse("")
          if(!regionId.equals(lastRegion.value())&& regionId.length>0){
            collector.collect(UserRegionFlow(1,regionId,gender,age))
            if(lastRegion.value()!=null){
              collector.collect(UserRegionFlow(0,lastRegion.value(),gender,age))
            }
            lastRegion.update(regionId)
          }
        }

        override def processBroadcastElement(in2: RegionCell, context: KeyedBroadcastProcessFunction[String, UserXdr, RegionCell, UserRegionFlow]#Context, collector: Collector[UserRegionFlow]): Unit = {
          val broadcastState = context.getBroadcastState(broadcastRegionCellDes)
          broadcastState.put(in2.laccell, in2.regionId)
        }
      })

    //按行政区做统计，按行政区keyby,  timeservice, 每一分钟输出一次统计结果。   状态保存行政区的人员构成统计
    val regionCalStream=userRegionFlowStream.keyBy(_.regionId).process(new KeyedProcessFunction[String,UserRegionFlow,RegionCal]() {
      var cal:ValueState[RegionCal]=_
      var isSetTime:ValueState[Boolean] = _

      override def open(parameters: Configuration): Unit = {
        super.open(parameters)
        val calDes=new ValueStateDescriptor[RegionCal]("cal",createTypeInformation[RegionCal])
        cal=getRuntimeContext.getState(calDes)

        val isSetTimeDes = new ValueStateDescriptor[Boolean]("isSetTime", createTypeInformation[Boolean])
        isSetTime = getRuntimeContext.getState(isSetTimeDes)
      }
      override def processElement(value: UserRegionFlow, context: KeyedProcessFunction[String, UserRegionFlow, RegionCal]#Context, collector: Collector[RegionCal]): Unit = {
        val regionCal=Option(cal.value()).getOrElse(RegionCal(value.regionId,0,0,0,0,0))
        val addNum=if(value.isIn==1) 1 else -1
        val gender=value.gender
        val age=value.age

        //开始统计
        if(gender==1){
          regionCal.manNum+=addNum
        }else{
          regionCal.womanNum+=addNum
        }
        if(age>=10 &&age<20){
          regionCal.age_10_20+=addNum
        }else if (age >= 20 && age < 40) {
          regionCal.age_20_40 += addNum
        } else if (age >= 40) {
          regionCal.age_40 += addNum
        }
        cal.update(regionCal)

        if(!Option(isSetTime.value()).getOrElse(false)){
          context.timerService().registerProcessingTimeTimer(10000)
          isSetTime.update(true)
        }
      }

      override def onTimer(timestamp: Long, ctx: KeyedProcessFunction[String, UserRegionFlow, RegionCal]#OnTimerContext, out: Collector[RegionCal]): Unit = {
        val regionCal=cal.value()
        out.collect(regionCal)
        isSetTime.update(false)
      }
    })
    regionCalStream.print()

    //第四步：将结果输出到HBase中
    val conf = new org.apache.hadoop.conf.Configuration()
    conf.set("hbase.zookeeper.quorum", "bigdata01:2181")
    conf.set("hbase.rootdir", "hdfs://bigdata01:9000/hbase")
    val hbaseSink = new HBaseSinkFunction[RegionCal]("user_persona",
      conf,
      new HBaseMutationConverter[RegionCal] {
        //初始化方法，只执行一次
        override def open(): Unit = {}

        //将Stream中的数据转化为HBase中的PUT操作
        override def convertToMutation(record: RegionCal): Mutation = {
          val rowkey = record.regionId
          val value = record
          val put = new Put(rowkey.getBytes())
          put.addColumn("persona".getBytes(), "man".getBytes(), value.manNum.toString.getBytes())
          put.addColumn("persona".getBytes(), "women".getBytes(), value.womanNum.toString.getBytes())
          put.addColumn("persona".getBytes(), "age_10_20".getBytes(), value.age_10_20.toString.getBytes())
          put.addColumn("persona".getBytes(), "age_20_40".getBytes(), value.age_20_40.toString.getBytes())
          put.addColumn("persona".getBytes(), "age_40".getBytes(), value.age_40.toString.getBytes())
          put
        }
      },
      100,
      100,
      1000
    )
    regionCalStream.addSink(hbaseSink)
    env.execute()




  }

}
