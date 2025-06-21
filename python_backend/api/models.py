from pydantic import BaseModel
from typing import List, Optional

class MsgResponse(BaseModel):
    msg: str = ""
    code: int = 200

class UserCountData(BaseModel):
    cnt: int

class UserCountResponse(MsgResponse):
    data: UserCountData

class UserListData(BaseModel):
    cnt: int
    userList: List[str]

class UserListResponse(MsgResponse):
    data: UserListData

class RegionPortraitData(BaseModel):
    regionId: str
    regionName: Optional[str] = None
    man: int
    women: int
    age_10_20: int
    age_20_40: int
    age_40: int # Represents 40+
    pepCnt: int

class RegionPortraitResponse(MsgResponse):
    data: RegionPortraitData

class FlowMetrics(BaseModel):
    total: int
    male: int
    female: int
    age_10_20: int
    age_20_40: int
    age_40_plus: int

class RegionInflowOutflowData(BaseModel):
    inflow: FlowMetrics
    outflow: FlowMetrics 