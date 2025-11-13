# 数据文件目录

此目录存放需要处理的数据文件。当此目录中的文件被推送到GitHub时，会自动触发数据处理流程。

## 文件格式

### 订单数据文件 (order_data.csv)
```csv
order_id,customer_id,amount,currency
O1001,C001,120,USD
O1002,C002,85,EUR
O1003,C003,150,CNY
O1004,C004,100,JPY
O1005,C001,90,USD
```

### 客户数据文件 (customer_data.csv)
```csv
customer_id,customer_name,region
C001,Alice,North
C002,Bob,West
C003,Chen,East
C004,Diana,South
```

## 自动处理流程

当此目录中的文件被修改并推送到GitHub时，GitHub Actions会自动：
1. 检测到data/目录中的文件变化
2. 运行`clean_and_merge.py`脚本
3. 更新数据库文件`merged_data.db`
4. 自动提交数据库变更

## 使用方法

1. 将新的数据文件放入此目录
2. 提交并推送更改到GitHub
3. 查看GitHub Actions运行状态
4. 数据库会自动更新