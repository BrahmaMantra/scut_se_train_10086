from typing import List, Optional
from pydantic import BaseModel


class UserRegionTimePortraitRequest(BaseModel):
    region_id: str
    produce_hour: str
    portrait_id: int


class UserCountData(BaseModel):
    cnt: int


class UserCountResponse(BaseModel):
    msg: str = ""
    code: int = 200
    data: UserCountData


class UserListData(BaseModel):
    cnt: int
    userList: List[int]


class UserListResponse(BaseModel):
    msg: str = ""
    code: int = 200
    data: UserListData


class RegionPortraitRequest(BaseModel):
    region_id: str


class RegionPortraitData(BaseModel):
    regionId: str
    regionName: Optional[str]
    man: int
    women: int
    age_10_20: int
    age_20_40: int
    age_40: int
    pepCnt: int


class RegionPortraitResponse(BaseModel):
    msg: str = ""
    code: int = 200
    data: RegionPortraitData
