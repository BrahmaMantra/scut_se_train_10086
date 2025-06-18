# db 表段定义

## clickhouse

- String：字符串类型
- Long/Int：整型
- ClickHouseBitmap/UInt32：RoaingBitmap 位图，底层为 ClickHouse 的 UInt32 类型集合

### 1. USER_INDEX

- 来源：core.CalUserBitmapIndex
- 字段：
  - IMSI (String)
  - BITMAP_ID (Long)

### 2. REGION_ID_IMSI_BITMAP

- 来源：core.CalRegionUserStay
- 字段：
  - REGION_ID (String)
  - PRODUCE_HOUR (String)
  - IMSI_INDEXES (ClickHouseBitmap/UInt32)

### 3. TA_PORTRAIT_IMSI_BITMAP

- 来源：core.CalUserPersonBitMap
- 字段：
  - PORTRAIT_ID (Int)
  - PORTRAIT_VALUE (String)
  - PORTRAIT_BITMAP (ClickHouseBitmap/UInt32)
  - COMMENT (String)

- 画像ID（PORTRAIT_ID）
  - 1：男性
  - 2：女性
  - 30：10-20岁
  - 40：20-40岁
  - 50：40岁以上
