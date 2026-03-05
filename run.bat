@echo off
echo 跨境电商热点网站启动中...
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
if not exist "requirements.txt" (
    echo 错误: 未找到requirements.txt
    pause
    exit /b 1
)

echo 安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告: 依赖安装失败，尝试继续运行...
)

REM 创建数据目录
if not exist "data" mkdir data

REM 初始化数据库
echo 初始化数据库...
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('数据库初始化完成')
"

REM 启动应用
echo 启动跨境电商热点网站...
echo 访问地址: http://localhost:5000
echo 按Ctrl+C停止应用
echo.
python app.py

pause