import pandas as pd
import pytest
from unittest.mock import patch
from pipeline import transform_customers, transform_orders

# 1. Test Customer
# ==========================================
@patch('pipeline.get_run_logger')
def test_transform_customers(mock_logger):
    raw_data = pd.DataFrame({
        'customer_id': [1, 2, 2],
        'full_name': ['Alice', 'Bob', 'Bob'],
        'email': ['alice@mail.com', None, ''],
        'phone': ['+1 (555) 123-4567', '12345abc', '9999'],
        'signup_date': ['2023-01-01', '2023-01-02', '2023-01-03']
    })
    
    cleaned_df = transform_customers.fn(raw_data)
    
    assert len(cleaned_df) == 2
    
    alice_phone = cleaned_df[cleaned_df['customer_id'] == 1]['phone'].iloc[0]
    assert alice_phone == '15551234567'
    
    bob_email = cleaned_df[cleaned_df['customer_id'] == 2]['email'].iloc[0]
    assert bob_email == 'unknown@domain.com'

# 2. Test Order
# ==========================================
@patch('pipeline.get_run_logger')
def test_transform_orders(mock_logger):
    orders_data = pd.DataFrame({
        'order_id': [101, 102],
        'customer_id': [1, 2],
        'order_date': ['2023-05-01', '2023-05-02'],
        'total_amount': [100.0, -50.0],  
        'currency': ['EUR', 'THB']
    })
    
    # จำลองข้อมูลเรทแลกเปลี่ยน
    rates_data = pd.DataFrame({
        'date': ['2023-05-01'],
        'currency': ['EUR'],
        'rate_to_usd': [1.1]
    })
    
    cleaned_df = transform_orders.fn(orders_data, rates_data)
    
    # ตรวจสอบผล
    assert len(cleaned_df) == 1
    assert cleaned_df['usd_amount'].iloc[0] == pytest.approx(110.0)