from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


# DTOs
class UserCountResponse(BaseModel):
    msg: str = ""
    code: int = 200
    data: dict


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


# APIs


@app.get("/v1/userCountByRegionAndTime", response_model=UserCountResponse)
def user_count_by_region_and_time(
    region_id: str = Query(...),
    produce_hour: str = Query(...),
    portrait_id: int = Query(...),
):
    # TODO: 实现具体逻辑
    return UserCountResponse(data={"cnt": 0})


@app.get("/v1/userListByRegionAndTime", response_model=UserListResponse)
def user_list_by_region_and_time(
    region_id: str = Query(...),
    produce_hour: str = Query(...),
    portrait_id: int = Query(...),
):
    # TODO: 实现具体逻辑
    return UserListResponse(data=UserListData(cnt=0, userList=[]))


@app.get("/v1/regionPortrait", response_model=RegionPortraitResponse)
def region_portrait(region_id: str = Query(...)):
    # TODO: 实现具体逻辑
    return RegionPortraitResponse(
        data=RegionPortraitData(
            regionId=region_id,
            regionName="",
            man=0,
            women=0,
            age_10_20=0,
            age_20_40=0,
            age_40=0,
            pepCnt=0,
        )
    )
