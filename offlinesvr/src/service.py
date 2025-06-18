import src.db.connection as conn
import src.api_models as models
from src.db_models import PortraitIdType


class Service:
    def query_user_count_by_region_and_time(
        self, region_id: str, produce_hour: str, portrait_id: int
    ) -> models.UserCountData:
        sql = """
WITH (
    SELECT
        IMSI_INDEXES
    FROM
        REGION_ID_IMSI_BITMAP
    WHERE
        REGION_ID = '{region_id:String}'
        AND PRODUCE_HOUR = '{produce_hour:String}'
) AS region_time_res
SELECT
    bitmapCardinality(bitmapAnd(region_time_res, PORTRAIT_BITMAP)) AS res
FROM
    TA_PORTRAIT_IMSI_BITMAP
WHERE
    PORTRAIT_ID = '{portrait_id:Long}';
        """
        paramaters = {
            "region_id": region_id,
            "produce_hour": produce_hour,
            "portrait_id": portrait_id,
        }
        client = conn.get_db_client()
        result = client.query(sql, parameters=paramaters)
        assert result.row_count == 1
        assert result.column_types.count == 1
        cnt = result.first_row[0]
        return models.UserCountData(cnt=cnt)

    def query_user_list_by_region_and_time(
        self, region_id: str, produce_hour: str, portrait_id: int
    ):
        sql = """
"WITH (
    SELECT
        IMSI_INDEXES
    FROM
        REGION_ID_IMSI_BITMAP
    WHERE
        REGION_ID = '{region_id:String}'
        AND PRODUCE_HOUR = '{produce_hour:String}') AS region_time_res
SELECT
    bitmapToArray(bitmapAnd(region_time_res,PORTRAIT_BITMAP)) AS res
FROM
    TA_PORTRAIT_IMSI_BITMAP
WHERE
    PORTRAIT_ID = {portrait_id:Long};
        """
        paramaters = {
            "region_id": region_id,
            "produce_hour": produce_hour,
            "portrait_id": portrait_id,
        }
        client = conn.get_db_client()
        result = client.query(sql, parameters=paramaters)
        cnt = result.row_count
        user_id_list = []
        for row in result.result_rows:
            user_id_list.append(row[0])
        return models.UserListData(cnt=cnt, userList=user_id_list)

    def query_region_protrait(self, region_id: str):
        sql = """
SELECT
    t2.PORTRAIT_ID,
    bitmapCardinality(bitmapAnd(t1.IMSI_INDEXES, t2.IMSI_INDEXES)) AS imsi_count
FROM
    REGION_ID_IMSI_BITMAP t1
JOIN
    TA_PORTRAIT_IMSI_BITMAP t2
ON 1 = 1
WHERE
    t1.REGION_ID = '{region_id:String}'
GROUP BY
    t2.PORTRAIT_ID
ORDER BY
    imsi_count
        """
        paramaters = {"region_id": region_id}
        data = models.RegionPortraitData(
            regionId="",
            regionName="",  # TODO: need to search?
            man=0,
            women=0,
            age_10_20=0,
            age_20_40=0,
            age_40=0,
            pepCnt=0,
        )
        client = conn.get_db_client()
        result = client.query(sql, parameters=paramaters)
        for row in result.result_rows:
            match row[0]:
                case PortraitIdType.Man:
                    data.man += 1
                case PortraitIdType.Women:
                    data.women += 1
                case PortraitIdType.TenToTwenty:
                    data.age_10_20 += 1
                case PortraitIdType.TwentyToForty:
                    data.age_20_40 += 1
                case PortraitIdType.UpperForty:
                    data.age_40 += 1
                case _:
                    pass
        data.pepCnt = result.row_count
        return data
