@echo off
title Python环境检查工具
echo ==========================================
echo      跨境电商热点网站 - Python环境检查
echo ==========================================
echo.

:: 设置错误处理
setlocal enabledelayedexpansion
set "ERROR_LEVEL=0"

:: 检查当前目录
echo [信息] 当前目录: %cd%
echo.

:: 1. 检查Python
echo [1/4] 检查Python命令...
where python >nul 2>&1
if errorlevel 1 (
    echo   状态: 未找到 python 命令
    set "PYTHON_CMD="
) else (
    echo   状态: 找到 python 命令
    set "PYTHON_CMD=python"
    echo   版本:
    python --version 2>nul || echo   无法获取版本信息
)

:: 2. 检查Python3
echo.
echo [2/4] 检查Python3命令...
where python3 >nul 2>&1
if errorlevel 1 (
    echo   状态: 未找到 python3 命令
    if not defined PYTHON_CMD set "PYTHON_CMD="
) else (
    echo   状态: 找到 python3 命令
    if not defined PYTHON_CMD set "PYTHON_CMD=python3"
    echo   版本:
    python3 --version 2>nul || echo   无法获取版本信息
)

:: 3. 检查py启动器
echo.
echo [3/4] 检查py启动器...
where py >nul 2>&1
if errorlevel 1 (
    echo   状态: 未找到 py 启动器
    if not defined PYTHON_CMD set "PYTHON_CMD="
) else (
    echo   状态: 找到 py 启动器
    if not defined PYTHON_CMD set "PYTHON_CMD=py"
    echo   版本:
    py --version 2>nul || echo   无法获取版本信息
)

:: 4. 检查pip
echo.
echo [4/4] 检查pip...
if defined PYTHON_CMD (
    echo   使用Python命令: %PYTHON_CMD%
    echo   检查pip可用性:
    %PYTHON_CMD% -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo   状态: pip不可用
        where pip >nul 2>&1
        if errorlevel 1 (
            echo   状态: 未找到独立pip命令
        ) else (
            echo   状态: 找到独立pip命令
            pip --version 2>nul || echo   无法获取版本信息
        )
    ) else (
        echo   状态: pip可用 (通过 %PYTHON_CMD% -m pip)
        %PYTHON_CMD% -m pip --version 2>nul || echo   无法获取版本信息
    )
) else (
    echo   状态: 未找到Python，跳过pip检查
)

:: 显示总结
echo.
echo ==========================================
echo                检查结果总结
echo ==========================================

if not defined PYTHON_CMD (
    echo ❌ 未找到任何Python版本
    echo.
    echo 解决方案：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载Python 3.7+安装包
    echo 3. 安装时务必勾选"Add Python to PATH"
    echo 4. 关闭所有命令行窗口，重新打开
) else (
    echo ✅ 找到Python: %PYTHON_CMD%
    echo.
    echo 可以尝试运行：
    echo   %PYTHON_CMD% --version
    echo   %PYTHON_CMD% -m pip --version
)

echo.
echo ==========================================
echo             下一步操作建议
echo ==========================================
echo.
echo 1. 如果已安装Python但仍显示未找到：
echo    - 重新安装Python，确保勾选"Add to PATH"
echo    - 重启计算机
echo.
echo 2. 如果Python已找到但pip不可用：
echo    - 运行: %PYTHON_CMD% -m ensurepip --upgrade
echo    - 或运行: %PYTHON_CMD% -m pip install --upgrade pip
echo.
echo 3. 安装项目依赖：
echo    - %PYTHON_CMD% -m pip install -r requirements_simple.txt
echo.
echo 4. 启动项目：
echo    - %PYTHON_CMD% app.py
echo    - 或双击 run_improved.bat
echo.
echo 5. 访问网站：
echo    - http://localhost:5000
echo.

echo 按任意键退出此窗口...
pause >nul