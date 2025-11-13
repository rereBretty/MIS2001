# GitHub Actions 工作流配置指南

## 📋 概述

本项目配置了自动化的数据处理流水线，当`data/`目录中的文件发生变化时，会自动触发数据处理流程并更新数据库。

## 🚀 工作流文件

### 位置
`.github/workflows/data_processing.yml`

### 触发条件
- **自动触发**: 当`data/`目录中的任何文件被推送时
- **手动触发**: 在GitHub仓库的Actions页面手动触发

### 执行步骤
1. **检出代码**: 使用`actions/checkout@v4`检出最新代码
2. **设置Python环境**: 使用Python 3.10
3. **安装依赖**: 安装requirements.txt中指定的包
4. **运行数据处理**: 执行`clean_and_merge.py`脚本
5. **提交变更**: 自动提交更新的数据库文件

## 📁 项目结构更新

```
项目根目录/
├── .github/
│   └── workflows/
│       └── data_processing.yml    # GitHub Actions工作流
├── data/                         # 数据文件目录
│   ├── order_data.csv           # 订单数据文件
│   ├── customer_data.csv        # 客户数据文件
│   └── README.md                # 数据目录说明
├── clean_and_merge.py           # 数据处理脚本
├── merged_data.db               # 生成的数据库文件
├── requirements.txt             # Python依赖包
└── README.md                    # 项目主说明文档
```

## 🔧 技术配置

### Python版本
- Python 3.10

### 依赖包
- Flask==2.3.3
- pandas==2.1.1

### 运行环境
- Ubuntu最新版本
- GitHub Actions托管的虚拟机

## 🎯 使用流程

### 1. 本地开发
```bash
# 将数据文件放入data/目录
cp your_data.csv data/

# 提交更改
git add data/
git commit -m "feat: add new data files"

# 推送触发工作流
git push origin main
```

### 2. 查看运行状态
- 访问GitHub仓库的"Actions"标签页
- 查看"Data Processing Pipeline"工作流的运行状态
- 查看执行日志和结果

### 3. 手动触发（可选）
- 在GitHub仓库的Actions页面
- 选择"Data Processing Pipeline"工作流
- 点击"Run workflow"手动触发

## 🔍 工作流详情

### 触发条件配置
```yaml
on:
  push:
    paths:
      - 'data/**'  # 仅当data/目录下的文件变化时触发
  workflow_dispatch:  # 支持手动触发
```

### 数据处理步骤
```yaml
- name: Run data processing script
  run: |
    python clean_and_merge.py
```

### 自动提交变更
```yaml
- name: Commit and push database changes
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git add merged_data.db
    git diff --staged --quiet || git commit -m "chore: update database from data processing pipeline"
    git push
```

## 📊 预期效果

1. **自动检测**: 当data/目录中的CSV文件被修改时自动触发
2. **数据处理**: 自动运行清理、合并、货币转换脚本
3. **数据库更新**: 生成最新的`merged_data.db`文件
4. **版本控制**: 自动提交数据库变更到Git仓库
5. **持续集成**: 确保数据库始终与最新数据同步

## 🔒 安全注意事项

- 工作流在GitHub托管的隔离环境中运行
- 使用只读权限检出代码
- 自动提交使用专用的GitHub Actions身份
- 不包含敏感信息或凭据

## 📞 故障排除

### 常见问题
1. **工作流未触发**: 检查文件路径是否在data/目录下
2. **依赖安装失败**: 检查requirements.txt格式和包版本
3. **脚本执行错误**: 查看工作流日志获取详细错误信息
4. **提交失败**: 检查Git权限配置

### 调试方法
- 查看GitHub Actions运行日志
- 在本地测试数据处理脚本
- 验证数据文件格式是否正确

## 🎉 成功标志

- GitHub Actions工作流显示绿色对勾
- 数据库文件`merged_data.db`被自动更新
- 提交历史中包含自动化提交记录
- 数据变化能够实时反映在Flask应用中