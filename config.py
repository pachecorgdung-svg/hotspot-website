import os

# 基础配置
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 环境检测
IS_VERCEL = os.environ.get('VERCEL') == '1'
IS_PRODUCTION = os.environ.get('ENVIRONMENT') == 'production' or IS_VERCEL

# Flask配置
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
DEBUG = not IS_PRODUCTION  # 生产环境关闭调试模式

# 数据库配置
if IS_VERCEL:
    # Vercel环境下使用/tmp目录（可写）
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/hot_spots.db'
else:
    # 本地开发环境
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "data", "hot_spots.db")}'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# 爬虫配置
CRAWLER_CONFIG = {
    'request_timeout': 10,
    'max_retries': 3,
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    ],
    'delay_range': (1, 3),  # 请求延迟范围（秒）
}

# 定时任务配置
SCHEDULER_CONFIG = {
    'daily_update_time': '09:00',  # 每天9点更新
    'timezone': 'Asia/Shanghai',
    'max_retries': 3,
}

# 热点评分配置
SCORE_CONFIG = {
    'site_weights': {
        '雨果网': 10,
        'AMZ123': 9,
        '新浪新闻': 8,
        '微博': 7,
        '知乎': 6,
        '抖音': 7,
        '小红书': 6,
    },
    'time_decay_hours': 72,  # 72小时内有效
    'title_length_optimal': (10, 50),  # 标题最佳长度范围
}

# 管理员配置（用于手动触发更新）
ADMIN_TOKEN = os.environ.get('UPDATE_TOKEN') or 'your-admin-token-change-this'