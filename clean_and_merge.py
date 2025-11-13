#!/usr/bin/env python3
"""
数据清理与合并脚本
功能：
1. 读取订单数据和客户数据
2. 清理重复数据
3. 转换金额为人民币
4. 合并数据到SQLite数据库
5. 创建按区域统计的平均金额汇总表
"""

import sqlite3
import pandas as pd
from io import StringIO

# 示例数据（可以替换为从文件读取）
order_data = """order_id,customer_id,amount,currency
O1001,C001,120,USD
O1002,C002,85,EUR
O1003,C003,150,CNY
O1004,C004,100,JPY
O1005,C001,90,USD"""

customer_data = """customer_id,customer_name,region
C001,Alice,North
C002,Bob,West
C003,Chen,East
C004,Diana,South"""


def clean_and_merge():
    """主函数：执行数据清理和合并操作"""
    
    # 1. 读取数据
    print("正在读取数据...")
    orders_df = pd.read_csv(StringIO(order_data))
    customers_df = pd.read_csv(StringIO(customer_data))
    
    print("原始订单数据:")
    print(orders_df)
    print("\n原始客户数据:")
    print(customers_df)
    
    # 2. 清理重复数据
    print("\n正在清理重复数据...")
    orders_cleaned = orders_df.drop_duplicates(subset=['order_id'])
    customers_cleaned = customers_df.drop_duplicates(subset=['customer_id'])
    
    print(f"清理后订单数: {len(orders_cleaned)}")
    print(f"清理后客户数: {len(customers_cleaned)}")
    
    # 3. 转换金额为人民币
    print("\n正在转换金额为人民币...")
    conversion_rates = {
        'USD': 6.9,
        'EUR': 7.5,
        'CNY': 1.0,
        'JPY': 0.05
    }
    
    orders_cleaned['amount_cny'] = orders_cleaned.apply(
        lambda row: row['amount'] * conversion_rates[row['currency']], 
        axis=1
    )
    
    print("转换后的订单数据:")
    print(orders_cleaned)
    
    # 4. 合并数据
    print("\n正在合并订单和客户数据...")
    merged_data = pd.merge(orders_cleaned, customers_cleaned, on='customer_id', how='left')
    
    print("合并后的数据:")
    print(merged_data)
    
    # 5. 写入SQLite数据库
    print("\n正在写入数据库...")
    conn = sqlite3.connect('merged_data.db')
    
    # 写入合并后的数据
    merged_data.to_sql('orders_with_customers', conn, if_exists='replace', index=False)
    
    # 6. 创建汇总表：按区域统计平均金额
    print("正在创建汇总表...")
    summary_data = merged_data.groupby('region')['amount_cny'].agg(['mean', 'count']).reset_index()
    summary_data.columns = ['region', 'avg_amount_cny', 'order_count']
    
    summary_data.to_sql('summary_by_region', conn, if_exists='replace', index=False)
    
    # 验证数据
    cursor = conn.cursor()
    
    print("\n数据库中的订单客户表:")
    cursor.execute("SELECT * FROM orders_with_customers")
    for row in cursor.fetchall():
        print(row)
    
    print("\n汇总表（按区域平均金额）:")
    cursor.execute("SELECT * FROM summary_by_region")
    for row in cursor.fetchall():
        print(row)
    
    conn.close()
    
    print(f"\n操作完成！数据已保存到 merged_data.db 文件中")
    print(f"- 主表: orders_with_customers")
    print(f"- 汇总表: summary_by_region")
    
    return merged_data, summary_data


def read_from_files(order_file_path, customer_file_path):
    """从文件读取数据的函数"""
    try:
        orders_df = pd.read_csv(order_file_path)
        customers_df = pd.read_csv(customer_file_path)
        return orders_df, customers_df
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
        return None, None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None, None


if __name__ == "__main__":
    # 使用方法1：使用示例数据
    print("=== 使用示例数据运行 ===")
    merged, summary = clean_and_merge()
    
    # 使用方法2：从文件读取（取消注释以下代码使用）
    """
    print("\n=== 从文件读取数据运行 ===")
    order_file = "order_data.csv"  # 替换为实际文件路径
    customer_file = "customer_data.csv"  # 替换为实际文件路径
    
    orders_df, customers_df = read_from_files(order_file, customer_file)
    if orders_df is not None and customers_df is not None:
        # 可以在这里调用处理函数，传入读取的数据
        pass
    """