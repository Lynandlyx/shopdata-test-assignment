import sqlite3
import pandas as pd
from prefect import task, flow, get_run_logger

SOURCE_DB = 'shopdata.db'
TARGET_DB = 'analytics.db'

# 1.Extract
# ==========================================
@task(name="Extract Data", retries=2)
def extract_data(query: str) -> pd.DataFrame :
    logger = get_run_logger()
    logger.info(f"Extracting data with query : {query}")
    try:
        with sqlite3.connect(SOURCE_DB) as conn :
            df = pd.read_sql_query(query, conn)
        logger.info(f"Successfully extracted {len(df)} rows.")
        return df
    except Exception as e :
        logger.error(f"Failed to extract data : {e}")
        raise e

# 2.Transform
# ==============================================
@task(name="Transform Customers")
def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Starting customer data transformation")
    
    df = df.sort_values(by='signup_date', ascending=False)
    df = df.drop_duplicates(subset=['customer_id'], keep='first')
    
    # Clean Phone Number
    df['phone'] = df['phone'].astype(str).str.replace(r'\D', '', regex=True)
    df['phone'] = df['phone'].replace(['nan', 'None', ''], None) 
    
    # Handle Missing Email
    df['email'] = df['email'].fillna('unknown@domain.com')
    df.loc[df['email'] == '', 'email'] = 'unknown@domain.com'
    
    logger.info(f"Transformed customers data to {len(df)} rows.")
    return df

@task(name="Transform Orders")
def transform_orders(orders_df: pd.DataFrame, rates_df: pd.DataFrame) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info("Starting order data transformation...")
    
    # ลบออเดอร์ที่ total_amount <= 0 
    initial_len = len(orders_df)
    orders_df = orders_df[orders_df['total_amount'] > 0].copy()
    logger.info(f"Filtered out {initial_len - len(orders_df)} invalid orders (<= 0).")
    
    # Currency Convert to USD
    # เชื่อมตาราง Orders กับ Exchange Rates using วันที่และสกุลเงิน
    merged_df = pd.merge(
        orders_df, 
        rates_df, 
        left_on=['order_date', 'currency'], 
        right_on=['date', 'currency'], 
        how='left'
    )
    
    # ถ้าไม่มีสกุลเงินให้ถือว่าเป็น USD 
    merged_df['rate_to_usd'] = merged_df['rate_to_usd'].fillna(1.0)
    
    # คำนวณเป็น USD 
    merged_df['usd_amount'] = merged_df['total_amount'] * merged_df['rate_to_usd']
    
    # ลบคอลัมน์ที่ไม่ได้ใช้ออกเพื่อ clean
    if 'date' in merged_df.columns:
        merged_df = merged_df.drop(columns=['date'])
    merged_df = merged_df.drop(columns=['rate_to_usd'])
    
    logger.info("Order data transformation complete.")
    return merged_df

# 3.Load
# ==========================================
@task(name="Load Data")
def load_data(df: pd.DataFrame, table_name: str):
    logger = get_run_logger()
    logger.info(f"Loading data into table: {table_name}...")
    try:
        with sqlite3.connect(TARGET_DB) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        logger.info(f"Successfully loaded {len(df)} rows into {table_name}.")
    except Exception as e:
        logger.error(f"Failed to load data into {table_name}: {e}")
        raise e

# Run Flow
# ==========================================
@flow(name="ShopData ETL Pipeline", log_prints=True)
def etl_pipeline():
    logger = get_run_logger()
    logger.info("=== Starting ETL Pipeline ===")
    
    # Extract
    raw_customers = extract_data("SELECT * FROM vw_raw_customers;")
    raw_orders = extract_data("SELECT * FROM vw_raw_orders;")
    exchange_rates = extract_data("SELECT * FROM vw_exchange_rates;")
    
    # Transform
    dim_customers = transform_customers(raw_customers)
    fct_orders = transform_orders(raw_orders, exchange_rates)
    
    # Load
    load_data(dim_customers, "dim_customers")
    load_data(fct_orders, "fct_orders")
    
    logger.info("=== ETL Pipeline Completed Successfully! ===")

if __name__ == "__main__":
    # Run Pipeline
    etl_pipeline()