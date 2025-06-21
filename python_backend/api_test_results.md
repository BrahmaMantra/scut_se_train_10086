# API 测试报告
本报告记录了对核心API的调用过程和返回结果。

## 1. 区域画像统计 (Region Portrait)
**请求:**
```bash
curl -X GET "http://127.0.0.1:8000/v1/regionPortrait?region_id=3747835140194172928"
```
**响应:**
```json
{"msg":"","code":200,"data":{"regionId":"3747835140194172928","regionName":null,"man":0,"women":2,"age_10_20":0,"age_20_40":0,"age_40":0,"pepCnt":2}}
```

## 2. 区域画像用户数统计 (User Count)
**请求:**
```bash
curl -X GET "http://127.0.0.1:8000/v1/userCountByRegionAndTime?region_id=3747835140194172928&produce_hour=2025062121&portrait_id=0"
```
**响应:**
```json
{"msg":"","code":200,"data":{"cnt":2}}
```

## 3. 区域画像用户明细 (User List)
**请求:**
```bash
curl -X GET "http://127.0.0.1:8000/v1/userListByRegionAndTime?region_id=3747835140194172928&produce_hour=2025062121&portrait_id=0"
```
**响应:**
```json
{"msg":"","code":200,"data":{"cnt":2,"userList":["b06a3c2d-39a4-4ae8-b4d6-fc041c5dae6a","eebcf2e8-bd7d-4de8-aa31-5fe1639fbd90"]}}
```

## 4. 区域流入流出分析 (Mocked)
**说明:** 此API返回的是预定义的模拟数据。
**请求:**
```bash
curl -X GET "http://127.0.0.1:8000/v1/regionInflowOutflow?region_id=3747835140194172928&start_time=2025062100&end_time=2025062123"
```
**响应:**
```json
[{"inflow":{"total":120,"male":70,"female":50,"age_10_20":20,"age_20_40":80,"age_40_plus":20},"outflow":{"total":100,"male":60,"female":40,"age_10_20":15,"age_20_40":70,"age_40_plus":15}}]
```

