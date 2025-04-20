with need_practice as(
    select practice_id
    from practices
    WHERE 
        dateadded >= UNIX_TIMESTAMP('2012-01-01 00:00:00') 
        AND dateadded <  UNIX_TIMESTAMP('2012-12-31 11:59:59');
),
order_status as(
    select practice_id, 
        CASE 
            WHEN product_line is "implants" or product_line is "crowns" or product_line is "bridges" THEN 'fixed'
            ELSE "removables" 
        END as category  
    from order
    where practice_id in need_practice
)

select practice_id, 
    count(case when  order_status.category = "fixed" then 1) as ""
from need_practice left join order_status on need_practice.practice_id = order_status.practice_id
group by need_practice.practice_id, order_status.category
