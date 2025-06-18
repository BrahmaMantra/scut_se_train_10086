### 离线分析相关 API

#### 1. 区域画像用户数统计（User Count By Region And Time）

- **接口描述**：统计指定区域、时间、画像特征下的用户数量。
- **请求方式**：GET
- **接口地址**：`/v1/userCountByRegionAndTime`
- **请求参数**：

  | 参数名          | 类型     | 必填 | 说明               |
      |--------------|--------|----|------------------|
  | region_id    | string | 是  | 区域唯一标识           |
  | produce_hour | string | 是  | 统计小时（yyyyMMddHH） |
  | portrait_id  | int    | 是  | 画像特征ID（如性别/年龄段）  |
- **请求示例**：
  ```shell
  curl -X GET "http://localhost:8080/v1/userCountByRegionAndTime?region_id=3747834968395481088&produce_hour=2025061100&portrait_id=5"
  ```
- **响应示例**：
  ```json
  {
    "msg": "",
    "code": 200,
    "data": {
      "cnt": 1
    }
  }
  ```

#### 2. 区域画像用户明细（User List By Region And Time）

- **接口描述**：查询指定区域、时间、画像特征下的用户明细（如IMSI列表）。
- **请求方式**：GET
- **接口地址**：`/v1/userListByRegionAndTime`
- **请求参数**：

  | 参数名          | 类型     | 必填 | 说明               |
      |--------------|--------|----|------------------|
  | region_id    | string | 是  | 区域唯一标识           |
  | produce_hour | string | 是  | 统计小时（yyyyMMddHH） |
  | portrait_id  | int    | 是  | 画像特征ID           |
- **请求示例**：
  ```shell
  curl -X GET "http://localhost:8080/v1/userListByRegionAndTime?region_id=3747834968395481088&produce_hour=2025061100&portrait_id=5"
  ```
- **响应示例**：
  ```json
  {
    "msg": "",
    "code": 200,
    "data": {
      "cnt": 1,
      "userList": [862]
    }
  }
  ```

#### 3. 区域画像统计（Region Portrait）

- **接口描述**：获取指定区域的用户画像统计信息（如性别、年龄段分布等）。
- **请求方式**：GET
- **接口地址**：`/v1/regionPortrait`
- **请求参数**：

  | 参数名       | 类型     | 必填 | 说明     |
    |-----------|--------|----|--------|
  | region_id | string | 是  | 区域唯一标识 |
- **请求示例**：
  ```shell
  curl -X GET "http://localhost:8080/v1/regionPortrait?region_id=3747834968395481088"
  ```
- **响应示例**：
  ```json
  {
    "msg": "",
    "code": 200,
    "data": {
      "regionId": "3747834968395481088",
      "regionName": "天河区栅格32",
      "man": 7,
      "women": 9,
      "age_10_20": 5,
      "age_20_40": 3,
      "age_40": 8,
      "pepCnt": 16
    }
  }
  ```

### TODO

#### 4. 全区域热力图（All Regions Heat Map）

- **接口描述**：获取所有区域的用户热力分布及画像统计。
- **请求方式**：GET
- **接口地址**：`/v1/allRegionsHeatMap`
- **请求参数**：无
- **请求示例**：
  ```shell
  curl -X GET "http://localhost:8080/v1/allRegionsHeatMap"
  ```
- **响应示例**：
  ```json
  {
    "msg": "",
    "code": 200,
    "data": {
      "statis": {
        "man": 1455,
        "women": 1485,
        "age_10_20": 645,
        "age_20_40": 1182,
        "age_40": 1113
      },
      "heatDataList": [
        {
          "regionId": "3747834968395481088",
          "center": ["113.29303973858326", "23.20150682574808"],
          "pepCnt": 16,
          "boundary": [ ... ]
        }
        // ...更多区域
      ]
    }
  }
  ```

#### 5. 区域流入流出人群离线分析（Region Inflow/Outflow Analysis）

- **接口描述**：获取指定区域在时间段内的流入、流出人群统计及画像分布。
- **请求方式**：GET
- **接口地址**：`/v1/regionInflowOutflow`
- **请求参数**：

  | 参数名        | 类型     | 必填 | 说明               |
    |------------|--------|----|------------------|
  | region_id  | string | 是  | 区域唯一标识           |
  | start_time | string | 是  | 开始时间（yyyyMMddHH） |
  | end_time   | string | 是  | 结束时间（yyyyMMddHH） |

- **响应示例**：
  ```json
  [
    {
      "inflow": {
        "total": 120,
        "male": 70,
        "female": 50,
        "age_10_20": 20,
        "age_20_40": 80,
        "age_40_plus": 20
      },
      "outflow": {
        "total": 100,
        "male": 60,
        "female": 40,
        "age_10_20": 15,
        "age_20_40": 70,
        "age_40_plus": 15
      }
    }
  ]
  ```
