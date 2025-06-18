from pydantic import BaseModel
from enum import Enum


class UserIndex(BaseModel):
    IMSI: str  # String
    BITMAP_ID: int  # Long


class RegionIdImsiBitmap(BaseModel):
    REGION_ID: str  # String
    PRODUCE_HOUR: int  # Long
    IMSI_INDEXES: int  # ClickHouseBitMap


class TaPortraitImsiBitmap(BaseModel):
    PORTRAIT_ID: int  # String
    PORTRAIT_VALUE: str  # String
    PORTRAIT_BITMAP: int  # ClickHouseBitMap
    COMMENT: str  # String


class PortraitIdType(Enum):
    Man = 1
    Women = 2
    TenToTwenty = 3
    TwentyToForty = 4
    UpperForty = 5
