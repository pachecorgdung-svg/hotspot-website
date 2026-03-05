#!/bin/bash

echo "检查Python环境..."
echo

# 检查Python
echo "1. 检查Python..."
if command -v python &> /dev/null; then
    echo "   找到python命令"
    python --version
else
    echo "   未找到python命令"
fi

echo
echo "2. 检查Python3..."
if command -v python3 &> /dev/null; then
    echo "   找到python3命令"
    python3 --version
else
    echo "   未找到python3命令"
fi

echo
echo "3. 检查pip..."
if command -v pip &> /dev/null; then
    echo "   找到pip命令"
    pip --version
elif command -v pip3 &> /dev/null; then
    echo "   找到pip3命令"
    pip3 --version
else
    echo "   未找到pip命令"
fi

echo
echo "4. 检查虚拟环境..."
if [ -d "venv" ] || [ -d ".venv" ]; then
    echo "   找到虚拟环境目录"
else
    echo "   未找到虚拟环境目录"
fi

echo
echo "环境检查完成。"
echo
echo "如果未找到Python，请按以下步骤安装："
echo "1. 访问 https://www.python.org/downloads/"
echo "2. 下载Python 3.7+安装包"
echo "3. 安装时确保添加到PATH（Linux/Mac通常自动添加）"
echo "4. 重新打开终端窗口"
echo
echo "对于Linux用户，可以使用包管理器安装："
echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
echo "  macOS: brew install python"
echo