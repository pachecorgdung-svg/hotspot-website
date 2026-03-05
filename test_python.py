#!/usr/bin/env python
"""测试Python环境是否能正常运行"""

import sys

def test_python_environment():
    """测试Python环境"""
    print("=" * 60)
    print("Python环境测试")
    print("=" * 60)

    # 1. Python版本
    print(f"1. Python版本: {sys.version}")
    print(f"   Python路径: {sys.executable}")

    # 2. 检查关键模块
    modules_to_check = [
        "flask", "sqlalchemy", "requests", "bs4",  # beautifulsoup4
        "apscheduler", "datetime", "json", "os", "sys"
    ]

    print("\n2. 检查关键模块:")
    missing_modules = []
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"   ✓ {module}")
        except ImportError:
            print(f"   ✗ {module} (未安装)")
            missing_modules.append(module)

    # 3. 检查文件权限
    print("\n3. 检查文件权限:")
    import os
    data_dir = "data"
    if os.path.exists(data_dir):
        if os.access(data_dir, os.W_OK):
            print(f"   ✓ 数据目录可写入: {data_dir}")
        else:
            print(f"   ✗ 数据目录不可写入: {data_dir}")
    else:
        try:
            os.makedirs(data_dir, exist_ok=True)
            print(f"   ✓ 数据目录已创建: {data_dir}")
        except Exception as e:
            print(f"   ✗ 无法创建数据目录: {e}")

    # 4. 总结
    print("\n" + "=" * 60)
    print("测试总结:")

    if missing_modules:
        print(f"缺少 {len(missing_modules)} 个模块: {', '.join(missing_modules)}")
        print("\n安装建议:")
        if "flask" in missing_modules:
            print("  pip install flask flask-sqlalchemy")
        if "requests" in missing_modules or "bs4" in missing_modules:
            print("  pip install requests beautifulsoup4 lxml")
        if "apscheduler" in missing_modules:
            print("  pip install apscheduler python-dateutil pytz")
        print("\n或安装所有依赖:")
        print("  pip install -r requirements_simple.txt")
    else:
        print("✓ 所有关键模块已安装，环境准备就绪！")
        print("\n可以运行: python app.py")

    print("=" * 60)

if __name__ == "__main__":
    try:
        test_python_environment()
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        print("\n可能Python环境有问题，请检查安装。")
        input("\n按Enter键退出...")