import sqlite3
import pandas as pd

conn = sqlite3.connect('analytics.db')

with open('clv_report.sql', 'r', encoding='utf-8') as file:
    query = file.read()

df = pd.read_sql_query(query, conn)

print("\n=== Customer Lifetime Value (CLV) Report ===")
print(df.to_string())
print("===============================================\n")

conn.close()