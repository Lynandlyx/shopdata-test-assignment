select customer_id, COUNT(*) AS record_count
from vw_raw_customers
group by customer_id
having COUNT(*) > 1;

select COUNT(*) AS missing_email_count
from vw_raw_customers
where email is null or email = '';

select customer_id, phone
from vw_raw_customers
where phone like '%+%' or phone like '%-%' or phone like '%(%';

where order_id, customer_id, total_amount
from vw_raw_orders
where total_amount <= 0;

select COUNT(*) as missing_currency_count
from vw_raw_orders
where currency is null or currency = '';