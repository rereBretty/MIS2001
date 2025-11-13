# 数据监控与展示系统

这是一个基于Flask和SQLite的数据监控与展示系统，支持实时数据更新和可视化展示。

## 功能特性

- ✅ 连接SQLite数据库
- ✅ 显示合并的订单数据表
- ✅ 显示按区域统计的平均金额汇总表
- ✅ 支持自动更新（AJAX轮询，每5秒检查一次）
- ✅ 响应式设计，支持移动端
- ✅ 实时数据统计卡片

## 项目结构

```
项目根目录/
├── app.py                 # Flask应用主文件
├── clean_and_merge.py     # 数据处理脚本
├── order_data.csv         # 订单数据文件
├── customer_data.csv      # 客户数据文件
├── merged_data.db         # 生成的SQLite数据库
├── templates/
│   └── index.html        # 前端界面模板
├── requirements.txt       # 依赖包列表
└── README.md             # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 生成数据（首次运行）

```bash
python clean_and_merge.py
```

这将生成 `merged_data.db` 数据库文件。

### 3. 启动Flask应用

```bash
python app.py
```

### 4. 访问应用

打开浏览器访问：http://127.0.0.1:5000

## 使用说明

### 数据处理流程

1. **数据准备**：将订单数据和客户数据分别保存为CSV文件
2. **数据清理**：去除重复数据，转换货币为人民币
3. **数据合并**：通过customer_id关联订单和客户数据
4. **数据库存储**：将处理后的数据存入SQLite数据库

### 前端界面功能

- **统计卡片**：显示总订单数、总客户数、总金额(CNY)、数据状态
- **订单数据表**：显示完整的合并订单数据
- **汇总数据表**：按区域统计平均金额和订单数量
- **自动更新**：当数据库文件发生变化时自动刷新数据

### API接口

- `GET /api/data` - 获取所有数据（订单表和汇总表）
- `GET /api/check_update` - 检查数据是否更新

## 技术栈

- **后端**：Flask、SQLite、Python
- **前端**：HTML5、CSS3、JavaScript、Bootstrap 5、Font Awesome
- **数据处理**：pandas、sqlite3

## 开发说明

### 自定义数据

如果要使用自定义数据，可以：

1. 修改 `order_data.csv` 和 `customer_data.csv` 文件
2. 运行 `python clean_and_merge.py` 重新生成数据库
3. 刷新浏览器查看更新后的数据

### 修改自动更新频率

在 `templates/index.html` 中修改以下代码：

```javascript
// 当前设置为每5秒检查一次
setInterval(() => {
    // 检查更新逻辑
}, 5000); // 修改此数值（毫秒）来调整频率
```

## 注意事项

- 确保数据库文件 `merged_data.db` 存在，否则应用会显示错误
- 应用会自动检测数据库文件的变化并更新界面
- 支持跨域访问，可以部署到服务器供多用户使用

## 部署选项

### 本地部署

```bash
python app.py
```

### 生产环境部署

建议使用Gunicorn + Nginx进行生产环境部署：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```