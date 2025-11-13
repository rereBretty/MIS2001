#!/usr/bin/env python3
"""
Flask应用 - 数据监控与展示系统
功能：
1. 连接SQLite数据库
2. 显示合并的订单数据表
3. 显示按区域统计的平均金额汇总表
4. 支持自动更新（AJAX轮询）
"""

from flask import Flask, render_template, jsonify
import sqlite3
import os
import time
from datetime import datetime

# 创建Flask应用并正确配置模板目录
app = Flask(__name__, template_folder='templates')

# 数据库文件路径
DB_PATH = 'merged_data.db'

def get_database_connection():
    """获取数据库连接"""
    return sqlite3.connect(DB_PATH)

def get_last_modified_time():
    """获取数据库文件的最后修改时间"""
    if os.path.exists(DB_PATH):
        return os.path.getmtime(DB_PATH)
    return 0

def get_orders_data():
    """从数据库获取订单数据"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        # 获取订单数据
        cursor.execute("""
            SELECT order_id, customer_id, customer_name, amount, currency, 
                   amount_cny, region 
            FROM orders_with_customers
            ORDER BY order_id
        """)
        
        orders = []
        for row in cursor.fetchall():
            orders.append({
                'order_id': row[0],
                'customer_id': row[1],
                'customer_name': row[2],
                'amount': row[3],
                'currency': row[4],
                'amount_cny': round(row[5], 2),
                'region': row[6]
            })
        
        conn.close()
        return orders
    except Exception as e:
        print(f"获取订单数据时出错: {e}")
        return []

def get_summary_data():
    """从数据库获取汇总数据"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        # 获取汇总数据
        cursor.execute("""
            SELECT region, avg_amount_cny, order_count 
            FROM summary_by_region
            ORDER BY region
        """)
        
        summary = []
        for row in cursor.fetchall():
            summary.append({
                'region': row[0],
                'avg_amount_cny': round(row[1], 2),
                'order_count': row[2]
            })
        
        conn.close()
        return summary
    except Exception as e:
        print(f"获取汇总数据时出错: {e}")
        return []

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    """API接口：返回所有数据"""
    orders = get_orders_data()
    summary = get_summary_data()
    last_modified = get_last_modified_time()
    
    return jsonify({
        'orders': orders,
        'summary': summary,
        'last_modified': last_modified,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'database_exists': os.path.exists(DB_PATH)
    })

@app.route('/api/check_update')
def api_check_update():
    """API接口：检查数据更新"""
    current_time = time.time()
    last_modified = get_last_modified_time()
    
    return jsonify({
        'last_modified': last_modified,
        'current_time': current_time,
        'has_changed': last_modified > getattr(api_check_update, 'last_check', 0)
    })

# 初始化上次检查时间
api_check_update.last_check = 0

if __name__ == '__main__':
    # 确保数据库存在
    if not os.path.exists(DB_PATH):
        print("警告：数据库文件不存在，请先运行 clean_and_merge.py 生成数据")
    
    print("Flask应用启动中...")
    print("访问地址: http://127.0.0.1:5000")
    print("API接口: http://127.0.0.1:5000/api/data")
    
    app.run(debug=True, host='0.0.0.0', port=5000)