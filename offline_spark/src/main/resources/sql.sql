select
  case
  when gender=='1' then 1
  when gender=='0' then 2
  end as PORTRAIT_ID,
  gender as PORTRAIT_VALUE,
  case
    when gender=='1' then '男性'
    when gender=='0' then '女性'
    end as COMMENT,
  collect_set(BITMAP_ID)  as bitmapIds
from
tmp_res group by gender

union
select
case
when age_flag=='10' then 3
when age_flag=='20' then 4
when age_flag=='40' then 5
end as PORTRAIT_ID,
age_flag as PORTRAIT_VALUE,
case
when age_flag=='10' then '10——20岁'
when age_flag=='20' then '20-40岁'
when age_flag=='40' then '40岁以上'
end as COMMENT,
 collect_set(BITMAP_ID)  as bitmapIds

from tmp_res group by age_flag