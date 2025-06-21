import requests
import json
from typing import List, Dict, Any

# 假设 FastAPI 服务器正在此地址运行
API_BASE_URL = "http://127.0.0.1:8000/v1"

def get_region_portrait(region_id: str) -> Dict[str, Any]:
    """
    获取指定区域的用户画像统计信息，包括总人数、性别分布、年龄段分布等。
    当你需要了解一个【具体区域】的【人群构成】时，应使用此工具。
    此工具只需一个参数：区域的唯一标识(region_id)。
    """
    print(f"工具调用: get_region_portrait(region_id='{region_id}')")
    try:
        response = requests.get(f"{API_BASE_URL}/regionPortrait", params={"region_id": region_id})
        response.raise_for_status()  # 如果请求失败 (如 404, 500), 则会抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API请求失败: {e}"}

def get_user_count_by_region_and_time(region_id: str, produce_hour: str, portrait_id: int) -> Dict[str, Any]:
    """
    获取在【指定区域】、【指定小时】(格式为 yyyyMMddHH)、拥有【指定画像特征】的用户数量。
    当你需要查询一个【非常精确时间点】的【用户数量】时，应使用此工具。
    例如，查询某个区域昨天上午10点的男性用户数。
    """
    print(f"工具调用: get_user_count_by_region_and_time(region_id='{region_id}', produce_hour='{produce_hour}', portrait_id={portrait_id})")
    params = {
        "region_id": region_id,
        "produce_hour": produce_hour,
        "portrait_id": portrait_id
    }
    try:
        response = requests.get(f"{API_BASE_URL}/userCountByRegionAndTime", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API请求失败: {e}"}

def get_user_list_by_region_and_time(region_id: str, produce_hour: str, portrait_id: int) -> Dict[str, Any]:
    """
    获取在【指定区域】、【指定小时】(格式为 yyyyMMddHH)、拥有【指定画像特征】的用户IMSI明细列表。
    当你需要知道【具体是哪些用户】满足条件时，应使用此工具。
    """
    print(f"工具调用: get_user_list_by_region_and_time(region_id='{region_id}', produce_hour='{produce_hour}', portrait_id={portrait_id})")
    params = {
        "region_id": region_id,
        "produce_hour": produce_hour,
        "portrait_id": portrait_id
    }
    try:
        response = requests.get(f"{API_BASE_URL}/userListByRegionAndTime", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API请求失败: {e}"}

def get_region_inflow_outflow(region_id: str, start_time: str, end_time: str) -> List[Dict[str, Any]]:
    """
    获取指定区域在【一个时间段内】的流入、流出人群统计及画像分布（这是一个模拟数据的API）。
    当你需要分析一个区域的【人流动态变化】时，应使用此工具。
    需要提供开始时间和结束时间，格式均为 yyyyMMddHH。
    """
    print(f"工具调用: get_region_inflow_outflow(region_id='{region_id}', start_time='{start_time}', end_time='{end_time}')")
    params = {
        "region_id": region_id,
        "start_time": start_time,
        "end_time": end_time
    }
    try:
        response = requests.get(f"{API_BASE_URL}/regionInflowOutflow", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return [{"error": f"API请求失败: {e}"}]

# 你可以在这里添加一个简单的测试来验证工具是否能正常工作
if __name__ == '__main__':
    print("--- 测试API工具 ---")
    
    # 请确保你的 FastAPI 服务器正在运行
    # 并替换成一个你知道存在于数据库中的 region_id
    test_region_id = "3747835140194172928" 
    
    print("\n1. 测试 get_region_portrait:")
    portrait_data = get_region_portrait(test_region_id)
    print(json.dumps(portrait_data, indent=2, ensure_ascii=False))

    print("\n2. 测试 get_region_inflow_outflow (模拟数据):")
    inflow_outflow_data = get_region_inflow_outflow(test_region_id, "2025010108", "2025010110")
    print(json.dumps(inflow_outflow_data, indent=2, ensure_ascii=False)) 