from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
v1_router = APIRouter(prefix="/v1")


# DTOs


class UserRegionTimePortraitRequest(BaseModel):
    region_id: str
    produce_hour: str
    portrait_id: int


class RegionPortraitRequest(BaseModel):
    region_id: str


class UserCountData(BaseModel):
    cnt: int = 0


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


# v1 路由组
@v1_router.get("/userCountByRegionAndTime")
def user_count_by_region_and_time(req: UserRegionTimePortraitRequest = Depends()):
    # req.region_id, req.produce_hour, req.portrait_id 可直接使用
    return {"msg": "", "code": 200, "data": {"cnt": 0}}


@v1_router.get("/userListByRegionAndTime")
def user_list_by_region_and_time(req: UserRegionTimePortraitRequest = Depends()):
    return {"msg": "", "code": 200, "data": {"cnt": 0, "userList": []}}


@v1_router.get("/regionPortrait")
def region_portrait(req: RegionPortraitRequest = Depends()):
    return {
        "msg": "",
        "code": 200,
        "data": {
            "regionId": req.region_id,
            "regionName": "",
            "man": 0,
            "women": 0,
            "age_10_20": 0,
            "age_20_40": 0,
            "age_40": 0,
            "pepCnt": 0,
        },
    }


app.include_router(v1_router)
