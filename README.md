# 跨境电商热点自动展示网站

一个自动抓取和展示跨境电商热点事件的网站，每天上午9点自动更新10大热点事件。

## 功能特点

- **自动抓取**：每天9:00自动从多个数据源抓取跨境电商热点
- **智能排序**：基于热度算法自动筛选Top10热点事件
- **美观展示**：响应式卡片设计，支持移动端和桌面端
- **定时任务**：使用APScheduler实现自动定时更新
- **API接口**：提供RESTful API接口，方便开发者使用
- **数据持久化**：使用SQLite数据库存储热点数据

## 技术栈

- **后端**：Python Flask + SQLAlchemy + APScheduler
- **前端**：HTML5 + CSS3 + JavaScript + Jinja2模板
- **数据库**：SQLite
- **爬虫**：Requests + BeautifulSoup4
- **定时任务**：APScheduler

## 数据来源

1. **跨境电商平台**：雨果网、AMZ123
2. **新闻媒体**：新浪新闻、搜狐新闻、腾讯新闻
3. **社交媒体**：微博、知乎、抖音、小红书

## 项目结构

```
cross-border-hotspots/
├── app.py                 # Flask主应用
├── requirements.txt       # Python依赖包
├── config.py             # 配置文件
├── README.md             # 项目说明
├── database/             # 数据库模块
│   ├── models.py         # 数据库模型
│   └── db_manager.py     # 数据库操作
├── crawler/              # 爬虫模块
│   ├── base_crawler.py   # 爬虫基类
│   ├── yuguo_crawler.py  # 雨果网爬虫
│   ├── news_crawler.py   # 新闻网站爬虫
│   └── social_crawler.py # 社交媒体爬虫
├── scheduler/            # 定时任务模块
│   └── tasks.py          # 定时任务配置
├── utils/                # 工具模块
│   ├── text_cleaner.py   # 文本清洗
│   └── scorer.py         # 热点评分
├── static/               # 静态文件
│   ├── css/
│   │   └── style.css     # 样式文件
│   └── js/
│       └── main.js       # 前端交互
├── templates/            # 模板文件
│   ├── base.html         # 基础模板
│   ├── index.html        # 主页模板
│   └── about.html        # 关于页面
└── data/                 # 数据目录
    └── hot_spots.db      # SQLite数据库
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.7+，然后安装依赖：

```bash
# 克隆项目
git clone <repository-url>
cd hotspot-website

# 安装依赖
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
# 创建数据目录
mkdir -p data

# 运行应用初始化数据库
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('数据库初始化完成')
"
```

### 3. 运行应用

```bash
# 启动Flask应用
python app.py
```

### 4. 访问应用

- 网站地址：http://localhost:5000
- API接口：http://localhost:5000/api/hotspots/today
- 关于页面：http://localhost:5000/about
- 健康检查：http://localhost:5000/health

## API接口

### 获取今日Top10热点
```
GET /api/hotspots/today
```

### 获取最近热点
```
GET /api/hotspots/recent?limit=20
```

### 获取统计数据
```
GET /api/stats
```

### 手动触发更新（需要认证）
```
POST /api/hotspots/update
Headers: X-Auth-Token: your-admin-token-change-this
```

### 获取热点详情
```
GET /api/hotspots/{id}
```

## 定时任务

系统配置了每天9:00自动更新热点数据：

- 定时任务使用APScheduler实现
- 时区配置为Asia/Shanghai
- 更新失败时自动重试3次
- 更新日志记录在控制台

### 手动测试定时任务

```bash
# 运行定时任务测试
python -c "from scheduler.tasks import test_update; test_update()"
```

## 配置说明

### 主要配置项（config.py）

- `SQLALCHEMY_DATABASE_URI`：数据库连接URI
- `SCHEDULER_CONFIG['daily_update_time']`：每日更新时间
- `ADMIN_TOKEN`：API认证令牌
- `CRAWLER_CONFIG`：爬虫配置
- `SCORE_CONFIG`：热点评分配置

### 自定义数据源

要添加新的数据源，只需：

1. 在`crawler/`目录中创建新的爬虫类，继承`BaseCrawler`
2. 实现`crawl()`方法
3. 在`app.py`的`crawlers`列表中添加新爬虫实例

### 调整热度算法

热点评分算法在`utils/scorer.py`中，可以调整：

1. 网站权重（`site_weights`）
2. 分类权重（`category_weights`）
3. 时间衰减参数
4. 互动数据加权系数

## 开发说明

### 运行测试

```bash
# 测试爬虫
python -c "from crawler.yuguo_crawler import YuguoCrawler; c = YuguoCrawler(); print(c.crawl())"

# 测试数据库
python -c "from database.db_manager import DBManager; print(DBManager.get_statistics())"

# 测试热点评分
python -c "from utils.scorer import HotSpotScorer; s = HotSpotScorer(); print(s.calculate_score({'title':'测试'}))"
```

### 调试模式

```bash
# 设置调试模式
export FLASK_DEBUG=1
python app.py
```

### 生产部署

建议使用生产服务器：

```bash
# 安装gunicorn
pip install gunicorn

# 使用gunicorn运行
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 常见问题

### 1. 依赖安装失败

确保使用正确的Python版本（3.7+），可以尝试：

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. 数据库初始化失败

检查SQLite路径权限：

```bash
chmod 755 data
```

### 3. 定时任务不运行

检查时区配置和系统时间，确保APScheduler正常启动。

### 4. 爬虫无法获取数据

当前版本使用模拟数据，要使用真实爬虫需要：

1. 分析目标网站结构
2. 实现真实的HTML解析逻辑
3. 处理反爬虫机制（User-Agent、延迟、代理等）

## 扩展功能建议

1. **数据可视化**：添加热点趋势图表
2. **邮件订阅**：用户订阅每日热点邮件
3. **关键词订阅**：用户关注特定关键词的热点
4. **多语言支持**：支持英文热点
5. **移动端应用**：开发手机APP
6. **数据导出**：支持导出CSV/Excel格式
7. **用户反馈**：用户可以对热点进行评分

## 许可证

本项目仅供学习和参考使用。

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 联系方式

如有问题或建议，请提交Issue或联系项目维护者。