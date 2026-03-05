from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import threading
import time

from config import *
from database import db, DBManager
from crawler import YuguoCrawler, NewsCrawler, SocialCrawler, crawler_manager
from utils import HotSpotScorer, TextCleaner
from scheduler.tasks import scheduler, update_daily_hotspots

# 创建Flask应用
app = Flask(__name__)
app.config.from_object(__name__)

# 初始化数据库
db.init_app(app)
DBManager.init_app(app)

# 爬虫管理器已初始化（通过crawler_manager）

def run_crawlers():
    """运行所有爬虫并处理数据（包装器）"""
    return crawler_manager.run_all()

@app.route('/')
def index():
    """主页 - 显示今日Top10热点"""
    today_top10 = DBManager.get_today_top10()

    # 如果今天还没有数据，运行爬虫获取
    if not today_top10:
        today_top10 = run_crawlers()
        # 转换为字典格式
        today_top10 = [h.to_dict() if hasattr(h, 'to_dict') else h for h in today_top10]
    else:
        # 转换为字典格式
        today_top10 = [h.to_dict() for h in today_top10]

    # 获取统计数据
    stats = DBManager.get_statistics()

    return render_template('index.html',
                         hotspots=today_top10,
                         stats=stats,
                         last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/hotspots/today')
def api_today_hotspots():
    """API: 获取今日Top10热点"""
    today_top10 = DBManager.get_today_top10()
    result = [h.to_dict() for h in today_top10]
    return jsonify({
        'success': True,
        'count': len(result),
        'data': result,
        'last_update': datetime.now().isoformat()
    })

@app.route('/api/hotspots/recent')
def api_recent_hotspots():
    """API: 获取最近热点"""
    limit = request.args.get('limit', default=20, type=int)
    recent = DBManager.get_recent_hotspots(limit)
    result = [h.to_dict() for h in recent]
    return jsonify({
        'success': True,
        'count': len(result),
        'data': result
    })

@app.route('/api/hotspots/update', methods=['POST'])
def api_update_hotspots():
    """API: 手动触发更新"""
    # 简单认证
    token = request.headers.get('X-Auth-Token')
    if token != ADMIN_TOKEN:
        return jsonify({'success': False, 'error': '未授权'}), 401

    # 在新线程中运行爬虫，避免阻塞
    def run_in_thread():
        run_crawlers()

    thread = threading.Thread(target=run_in_thread)
    thread.start()

    return jsonify({
        'success': True,
        'message': '更新任务已启动',
        'start_time': datetime.now().isoformat()
    })

@app.route('/api/stats')
def api_stats():
    """API: 获取统计数据"""
    stats = DBManager.get_statistics()
    return jsonify({
        'success': True,
        'data': stats
    })

@app.route('/api/hotspots/<int:hotspot_id>')
def api_hotspot_detail(hotspot_id):
    """API: 获取热点详情"""
    hotspot = DBManager.get_hotspot_by_id(hotspot_id)
    if not hotspot:
        return jsonify({'success': False, 'error': '热点不存在'}), 404

    return jsonify({
        'success': True,
        'data': hotspot.to_dict()
    })

@app.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Cross-border E-commerce Hotspots'
    })

# Vercel适配：主程序入口
if __name__ == '__main__':
    # 本地运行模式
    import os

    # 确保数据目录存在（本地环境）
    if not IS_VERCEL:
        os.makedirs('data', exist_ok=True)

    # 启动定时任务调度器（仅本地运行，Vercel环境使用Cron Jobs）
    if not IS_VERCEL:
        scheduler.start()
        print("定时任务调度器已启动")
        print(f"定时任务配置: 每天 {SCHEDULER_CONFIG['daily_update_time']} 自动更新")
    else:
        print("Vercel环境：定时任务已禁用，建议配置Vercel Cron Jobs调用更新API")

    # 启动Flask应用
    print("跨境电商热点网站启动中...")
    print(f"访问地址: http://localhost:{os.environ.get('PORT', 5000)}")
    print(f"API地址: http://localhost:{os.environ.get('PORT', 5000)}/api/hotspots/today")

    # 使用环境变量PORT或默认5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=DEBUG, host='0.0.0.0', port=port)