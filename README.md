# Data Engineer Technical Assignment

## Part 1 : Data Exploration & Understanding (SQL)
After running the initial queries in 'exploration.sql' to the 'shopdata.db' I discovered 3 data quality issues :

1. **Duplicate Customer Records :** There are instances where the same `customer_id` appears multiple times in `vw_raw_customers`.
2. **Inconsistent Contact Information :** Several records have missing `email` fields. Additionally, the `phone` column contains improperly formatted numbers with non-numeric characters (e.g., `+1 (555) 123-4567`).
3. **System Errors in Order Amounts :** Identified invalid transactions in `vw_raw_orders` where the `total_amount` is less than or equal to zero.
