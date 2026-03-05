#!/bin/bash

echo "跨境电商热点网站启动中..."
echo

# 检查Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python 3.7+"
    echo "下载地址: https://www.python.org/downloads/"
    exit 1
fi

# 使用python3如果可用，否则使用python
PYTHON_CMD=python3
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD=python
fi

# 检查依赖
if [ ! -f "requirements.txt" ]; then
    echo "错误: 未找到requirements.txt"
    exit 1
fi

echo "安装依赖..."
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "警告: 依赖安装失败，尝试继续运行..."
fi

# 创建数据目录
mkdir -p data

# 初始化数据库
echo "初始化数据库..."
$PYTHON_CMD -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('数据库初始化完成')
"

# 启动应用
echo "启动跨境电商热点网站..."
echo "访问地址: http://localhost:5000"
echo "按Ctrl+C停止应用"
echo
$PYTHON_CMD app.py