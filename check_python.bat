@echo off
echo 检查Python环境...
echo.

REM 检查Python
echo 1. 检查Python...
where python >nul 2>&1
if errorlevel 1 (
    echo   未找到python命令
) else (
    echo   找到python命令
    python --version
)

echo.
echo 2. 检查Python3...
where python3 >nul 2>&1
if errorlevel 1 (
    echo   未找到python3命令
) else (
    echo   找到python3命令
    python3 --version
)

echo.
echo 3. 检查py启动器...
where py >nul 2>&1
if errorlevel 1 (
    echo   未找到py启动器
) else (
    echo   找到py启动器
    py --version
)

echo.
echo 4. 检查pip...
where pip >nul 2>&1
if errorlevel 1 (
    echo   未找到pip命令
) else (
    echo   找到pip命令
    pip --version
)

echo.
echo 环境检查完成。
echo.
echo 如果未找到Python，请按以下步骤安装：
echo 1. 访问 https://www.python.org/downloads/
echo 2. 下载Python 3.7+安装包
echo 3. 安装时勾选"Add Python to PATH"
echo 4. 重新打开命令行窗口
echo.
pause