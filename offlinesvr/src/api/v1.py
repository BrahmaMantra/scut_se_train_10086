from fastapi import APIRouter, Depends
import api_models as m
from service import Service

router = APIRouter()


@router.get("/userCountByRegionAndTime")
def user_count_by_region_and_time(req: m.UserRegionTimePortraitRequest = Depends()):
    # req.region_id, req.produce_hour, req.portrait_id 可直接使用
    data = Service().query_user_count_by_region_and_time(
        req.region_id, req.produce_hour, req.portrait_id
    )
    return m.UserCountResponse(data=data)


@router.get("/userListByRegionAndTime")
def user_list_by_region_and_time(req: m.UserRegionTimePortraitRequest = Depends()):
    data = Service().query_user_list_by_region_and_time(
        req.region_id, req.produce_hour, req.portrait_id
    )
    return m.UserListResponse(data=data)


@router.get("/regionPortrait")
def region_portrait(req: m.RegionPortraitRequest = Depends()):
    data = Service().query_region_protrait(req.region_id)
    return m.RegionPortraitResponse(data=data)
