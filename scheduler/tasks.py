from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import time
import logging

from config import SCHEDULER_CONFIG, IS_VERCEL
from crawler.manager import crawler_manager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建调度器
scheduler = BackgroundScheduler(timezone=SCHEDULER_CONFIG['timezone'])

def update_daily_hotspots():
    """每日更新热点任务"""
    logger.info(f"开始执行每日热点更新任务 - {datetime.now()}")

    try:
        # 运行爬虫
        hotspots = crawler_manager.run_all()
        logger.info(f"热点更新完成，共获取 {len(hotspots)} 个热点")

        return True
    except Exception as e:
        logger.error(f"热点更新失败: {e}")
        # 重试逻辑
        for attempt in range(SCHEDULER_CONFIG['max_retries'] - 1):
            try:
                logger.info(f"第 {attempt + 2} 次重试...")
                time.sleep(60 * (attempt + 1))  # 等待时间递增
                hotspots = crawler_manager.run_all()
                logger.info(f"重试成功，获取 {len(hotspots)} 个热点")
                return True
            except Exception as retry_error:
                logger.error(f"重试 {attempt + 2} 失败: {retry_error}")

        logger.error(f"所有重试均失败")
        return False

def schedule_daily_update():
    """安排每日更新任务"""
    # 解析时间配置
    update_time = SCHEDULER_CONFIG['daily_update_time']
    hour, minute = map(int, update_time.split(':'))

    # 添加每日任务
    trigger = CronTrigger(hour=hour, minute=minute, timezone=SCHEDULER_CONFIG['timezone'])
    scheduler.add_job(
        update_daily_hotspots,
        trigger=trigger,
        id='daily_hotspot_update',
        name='每日热点更新',
        replace_existing=True
    )

    logger.info(f"已安排每日更新任务: {hour:02d}:{minute:02d}")

# 初始化时安排任务（Vercel环境不安排定时任务，使用外部Cron Jobs）
if not IS_VERCEL:
    schedule_daily_update()
else:
    logger.info("Vercel环境检测：跳过定时任务安排，建议使用Vercel Cron Jobs调用更新API")

# 测试函数
def test_update():
    """测试更新任务"""
    logger.info("手动测试更新任务...")
    result = update_daily_hotspots()
    logger.info(f"测试更新结果: {'成功' if result else '失败'}")
    return result

if __name__ == '__main__':
    # 直接运行此文件可以测试定时任务
    print("测试定时任务模块...")
    scheduler.start()
    print("调度器已启动")

    # 立即运行一次测试
    test_update()

    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("调度器已关闭")