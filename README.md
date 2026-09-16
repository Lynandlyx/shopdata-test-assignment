# Data Engineer Technical Assignment

## Data Exploration & Understanding (SQL)
After running the initial queries in `exploration.sql` to the `shopdata.db` I discovered 3 data quality issues :

1. **Duplicate Customer Records :** There are instances where the same `customer_id` appears multiple times in `vw_raw_customers`.
2. **Inconsistent Contact Information :** Several records have missing `email` fields. Additionally, the `phone` column contains improperly formatted numbers with non-numeric characters (e.g., `+1 (555) 123-4567`).
3. **System Errors in Order Amounts :** Identified invalid transactions in `vw_raw_orders` where the `total_amount` is less than or equal to zero.

## How to Run the Project

**1.Setup Environment**
Ensure you have Python installed, then install the dependencies :
```bash
pip install -r requirements.txt
```

**2.Run the ETL Pipeline**
To extract, transform, and load the data from `shopdata.db` into `analytics.db` :
```bash
python pipeline.py
```

**3. Run Unit Tests**
To verify the data cleaning logic in isolation (handling of duplicates, phone number formatting, and currency conversion), run :
```bash
pytest test_pipeline.py -v
```

**4. Generate CLV Report**
After the ETL pipeline completes successfully, run the query provided in clv_report.sql against the newly generated analytics.db to view the Customer Lifetime Value rankings.
(Optional : You can also quickly test and view the SQL report output by running python test_clv.py in the terminal).
```bash
python test_clv.py
```

