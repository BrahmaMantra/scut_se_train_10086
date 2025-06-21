from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timedelta
import mysql.connector
from typing import List

from . import models
from .database import get_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Analysis API"}

@app.get("/v1/userCountByRegionAndTime", response_model=models.UserCountResponse)
def get_user_count(region_id: str, produce_hour: str, portrait_id: int, db: mysql.connector.connect = Depends(get_db_connection)):
    try:
        hour_dt = datetime.strptime(produce_hour, "%Y%m%d%H")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid produce_hour format. Use yyyyMMddHH.")

    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed.")

    cursor = db.cursor()
    query = """
        SELECT COUNT(hru.imsi)
        FROM hourly_region_users hru
        JOIN user_profiles up ON hru.imsi = up.imsi
        WHERE hru.region_id = %s
          AND hru.produce_hour = %s
          AND (up.gender = %s OR up.age_group = %s)
    """
    try:
        # Assuming portrait_id can be for either gender or age
        # A more robust system might have separate parameters for these
        cursor.execute(query, (region_id, hour_dt, portrait_id, portrait_id))
        count = cursor.fetchone()[0]
        return models.UserCountResponse(data=models.UserCountData(cnt=count))
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query failed: {err}")
    finally:
        cursor.close()
        db.close()


@app.get("/v1/userListByRegionAndTime", response_model=models.UserListResponse)
def get_user_list(region_id: str, produce_hour: str, portrait_id: int, db: mysql.connector.connect = Depends(get_db_connection)):
    try:
        hour_dt = datetime.strptime(produce_hour, "%Y%m%d%H")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid produce_hour format. Use yyyyMMddHH.")

    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed.")

    cursor = db.cursor()
    query = """
        SELECT hru.imsi
        FROM hourly_region_users hru
        JOIN user_profiles up ON hru.imsi = up.imsi
        WHERE hru.region_id = %s
          AND hru.produce_hour = %s
          AND (up.gender = %s OR up.age_group = %s)
    """
    try:
        cursor.execute(query, (region_id, hour_dt, portrait_id, portrait_id))
        users = [item[0] for item in cursor.fetchall()]
        return models.UserListResponse(data=models.UserListData(cnt=len(users), userList=users))
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query failed: {err}")
    finally:
        cursor.close()
        db.close()


@app.get("/v1/regionPortrait", response_model=models.RegionPortraitResponse)
def get_region_portrait(region_id: str, db: mysql.connector.connect = Depends(get_db_connection)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed.")

    cursor = db.cursor(dictionary=True)
    
    # Find the most recent hour of data available for any region
    cursor.execute("SELECT MAX(produce_hour) FROM hourly_region_users")
    latest_hour = cursor.fetchone()['MAX(produce_hour)']
    
    if not latest_hour:
        raise HTTPException(status_code=404, detail="No aggregated data found.")

    query = """
        SELECT
            up.gender,
            up.age_group,
            COUNT(up.imsi) as count
        FROM hourly_region_users hru
        JOIN user_profiles up ON hru.imsi = up.imsi
        WHERE hru.region_id = %s AND hru.produce_hour = %s
        GROUP BY up.gender, up.age_group
    """
    try:
        cursor.execute(query, (region_id, latest_hour))
        results = cursor.fetchall()

        portrait = {
            "man": 0, "women": 0,
            "age_10_20": 0, "age_20_40": 0, "age_40": 0
        }

        for row in results:
            if row['gender'] == 1: # Assuming 1 is male
                portrait['man'] += row['count']
            elif row['gender'] == 0: # Assuming 0 is female
                portrait['women'] += row['count']
            
            # Assuming age_group mappings: 2->10-20, 3->20-40, 4->40+
            if row['age_group'] == 2:
                portrait['age_10_20'] += row['count']
            elif row['age_group'] == 3:
                portrait['age_20_40'] += row['count']
            elif row['age_group'] == 4:
                portrait['age_40'] += row['count']
        
        pepCnt = sum(portrait.values())

        data = models.RegionPortraitData(
            regionId=region_id,
            pepCnt=pepCnt,
            **portrait
        )
        return models.RegionPortraitResponse(data=data)

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query failed: {err}")
    finally:
        cursor.close()
        db.close()


@app.get("/v1/regionInflowOutflow", response_model=List[models.RegionInflowOutflowData])
def get_region_inflow_outflow(region_id: str, start_time: str, end_time: str):
    # This is a placeholder. A real implementation would require a much more
    # complex data processing job and table structure (e.g., the proposed
    # 'daily_region_flow' table). The complexity of calculating this on-the-fly
    # from raw events is too high for a production API.
    # We return a mocked response that matches the API documentation.
    
    return [
        {
          "inflow": {
            "total": 120, "male": 70, "female": 50,
            "age_10_20": 20, "age_20_40": 80, "age_40_plus": 20
          },
          "outflow": {
            "total": 100, "male": 60, "female": 40,
            "age_10_20": 15, "age_20_40": 70, "age_40_plus": 15
          }
        }
    ] 