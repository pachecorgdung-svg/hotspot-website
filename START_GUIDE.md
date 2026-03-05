# 跨境电商热点网站 - 启动指南

如果您遇到"localhost已拒绝连接"或无法启动的问题，请按照本指南解决。

## 快速解决方案

### 方案1：检查并安装Python（推荐）
1. **运行环境检查工具**：
   - Windows: 双击 `check_python.bat`
   - Mac/Linux: 在终端运行 `python3 --version`

2. **安装Python 3.7+**：
   - 访问 [Python官网](https://www.python.org/downloads/)
   - 下载最新版本（3.7或更高）
   - **重要**：安装时勾选 **"Add Python to PATH"**

3. **验证安装**：
   ```bash
   python --version
   # 或
   python3 --version
   ```

### 方案2：使用简化依赖
如果安装完整依赖失败，尝试简化版：

1. 使用简化依赖文件：
   ```bash
   pip install -r requirements_simple.txt
   ```

2. 然后运行：
   ```bash
   python app.py
   ```

### 方案3：使用Docker（需要安装Docker）
如果已安装Docker：

1. 构建并运行：
   ```bash
   docker-compose up --build
   ```

2. 访问：http://localhost:5000

## 常见问题解决

### 问题1："python不是内部或外部命令"
**原因**：Python未安装或未添加到PATH环境变量。

**解决**：
1. 重新安装Python，确保勾选"Add Python to PATH"
2. 重启命令行窗口
3. 运行 `python --version` 验证

### 问题2："pip不是内部或外部命令"
**原因**：pip未安装或PATH问题。

**解决**：
1. 确保Python安装时包含了pip
2. 尝试 `python -m pip` 代替 `pip`
3. 重新安装Python

### 问题3：依赖安装失败（特别是pandas/numpy）
**原因**：某些包需要编译环境。

**解决**：
1. 使用简化依赖（去掉pandas/numpy）：
   ```bash
   pip install -r requirements_simple.txt
   ```

2. 或安装预编译版本：
   ```bash
   pip install pandas --prefer-binary
   ```

### 问题4：端口5000被占用
**原因**：其他程序正在使用5000端口。

**解决**：
1. 停止其他使用5000端口的程序
2. 或修改app.py中的端口号：
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # 改为5001
   ```

### 问题5：数据库权限错误
**原因**：无法创建或写入数据库文件。

**解决**：
1. 确保有数据目录写入权限
2. 手动创建data目录：
   ```bash
   mkdir data
   ```

## 分步启动流程

### Windows用户
1. 双击运行 `check_python.bat`
2. 根据检查结果安装/修复Python
3. 双击运行 `run.bat`
4. 如果失败，尝试手动：
   ```cmd
   pip install -r requirements_simple.txt
   python app.py
   ```

### Mac/Linux用户
1. 运行环境检查：
   ```bash
   chmod +x check_python.sh
   ./check_python.sh
   ```

2. 安装依赖：
   ```bash
   pip3 install -r requirements_simple.txt
   ```

3. 启动应用：
   ```bash
   python3 app.py
   ```

### Docker用户
1. 安装Docker和Docker Compose
2. 运行：
   ```bash
   docker-compose up --build
   ```
3. 访问 http://localhost:5000

## 验证应用运行

成功启动后，您应该看到：
```
跨境电商热点网站启动中...
访问地址: http://localhost:5000
API地址: http://localhost:5000/api/hotspots/today
定时任务配置: 每天 09:00 自动更新
```

### 测试连接
1. 打开浏览器访问：http://localhost:5000
2. 测试API：http://localhost:5000/api/hotspots/today
3. 健康检查：http://localhost:5000/health

## 故障排除检查清单

- [ ] Python 3.7+ 已安装并添加到PATH
- [ ] pip可正常使用
- [ ] 依赖安装成功（无红色错误信息）
- [ ] 端口5000未被占用
- [ ] data目录存在且有写入权限
- [ ] 防火墙未阻止本地连接

## 获取帮助

如果以上方法都无法解决问题：

1. **查看错误信息**：复制完整的错误信息
2. **检查日志**：查看命令行输出的详细错误
3. **环境信息**：
   - 操作系统版本
   - Python版本 (`python --version`)
   - pip版本 (`pip --version`)

将上述信息提供给技术支持人员。

## 备选方案

如果所有方法都失败，可以考虑：

1. **使用在线Python环境**（如Replit、GitHub Codespaces）
2. **使用虚拟机/容器**（如VirtualBox + Ubuntu）
3. **联系开发者**获取预配置环境

---

**注意**：本应用使用模拟数据，无需真实网络连接即可运行。所有功能都可在本地测试。