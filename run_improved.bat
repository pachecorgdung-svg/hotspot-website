@echo off
echo 跨境电商热点网站启动中...
echo.

REM 检查Python（尝试多个命令）
echo 检查Python环境...
where python >nul 2>&1
if errorlevel 1 (
    where python3 >nul 2>&1
    if errorlevel 1 (
        where py >nul 2>&1
        if errorlevel 1 (
            echo 错误: 未找到Python、Python3或py启动器
            echo.
            echo 请先安装Python 3.7+：
            echo 1. 访问 https://www.python.org/downloads/
            echo 2. 下载Python 3.7+安装包
            echo 3. 安装时务必勾选"Add Python to PATH"
            echo 4. 重新打开此命令行窗口
            echo.
            echo 也可以运行 check_python.bat 检查环境
            pause
            exit /b 1
        ) else (
            set PYTHON_CMD=py
        )
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

REM 显示Python版本
echo 使用命令: %PYTHON_CMD%
%PYTHON_CMD% --version
if errorlevel 1 (
    echo 警告: Python版本检查失败，尝试继续...
)

REM 检查依赖文件
if not exist "requirements_simple.txt" (
    if not exist "requirements.txt" (
        echo 错误: 未找到依赖文件 requirements.txt 或 requirements_simple.txt
        pause
        exit /b 1
    ) else (
        set REQ_FILE=requirements.txt
    )
) else (
    echo 使用简化依赖文件（跳过pandas/numpy）
    set REQ_FILE=requirements_simple.txt
)

echo.
echo 安装依赖（%REQ_FILE%）...
%PYTHON_CMD% -m pip install --upgrade pip
if errorlevel 1 (
    echo 警告: pip升级失败，尝试继续...
)

%PYTHON_CMD% -m pip install -r %REQ_FILE%
if errorlevel 1 (
    echo 警告: 依赖安装失败，尝试继续运行...
    echo 如果pandas/numpy安装失败，请确保已安装Visual Studio Build Tools
    echo 下载: https://visualstudio.microsoft.com/visual-cpp-build-tools/
)

REM 创建数据目录
if not exist "data" mkdir data

REM 初始化数据库
echo.
echo 初始化数据库...
%PYTHON_CMD% -c "
try:
    from app import app, db
    with app.app_context():
        db.create_all()
        print('数据库初始化完成')
except Exception as e:
    print(f'数据库初始化失败: {e}')
    print('尝试继续运行...')
"

REM 启动应用
echo.
echo 启动跨境电商热点网站...
echo 访问地址: http://localhost:5000
echo API地址: http://localhost:5000/api/hotspots/today
echo 按Ctrl+C停止应用
echo.

REM 检查端口占用
netstat -ano | findstr :5000 >nul
if not errorlevel 1 (
    echo 警告: 端口5000可能已被占用
    echo 如果无法访问，请检查是否有其他程序使用5000端口
    echo.
)

%PYTHON_CMD% app.py

echo.
echo 应用已停止。
pause