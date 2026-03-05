from datetime import datetime, timedelta
from sqlalchemy import desc, func
from .models import db, HotSpot

class DBManager:
    """数据库管理类"""

    @staticmethod
    def init_app(app):
        """初始化数据库"""
        db.init_app(app)
        with app.app_context():
            db.create_all()

    @staticmethod
    def add_hotspot(hotspot_data):
        """添加热点事件"""
        # 检查是否已存在（根据标题和来源）
        existing = HotSpot.query.filter_by(
            title=hotspot_data['title'],
            source_site=hotspot_data['source_site']
        ).first()

        if existing:
            # 更新现有记录
            for key, value in hotspot_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.updated_at = datetime.now()
            db.session.commit()
            return existing
        else:
            # 创建新记录
            hotspot = HotSpot(**hotspot_data)
            db.session.add(hotspot)
            db.session.commit()
            return hotspot

    @staticmethod
    def get_today_top10():
        """获取今日Top10热点"""
        today = datetime.now().date()
        return HotSpot.query.filter(
            HotSpot.is_today_top == True,
            func.date(HotSpot.crawl_date) == today
        ).order_by(desc(HotSpot.heat_score)).limit(10).all()

    @staticmethod
    def update_today_top10(hotspot_ids):
        """更新今日Top10标记"""
        # 清除旧的Top10标记
        HotSpot.query.update({HotSpot.is_today_top: False})

        # 设置新的Top10
        for hotspot_id in hotspot_ids:
            hotspot = HotSpot.query.get(hotspot_id)
            if hotspot:
                hotspot.is_today_top = True
                hotspot.updated_at = datetime.now()

        db.session.commit()

    @staticmethod
    def get_recent_hotspots(limit=20):
        """获取最近的热点事件"""
        return HotSpot.query.order_by(desc(HotSpot.crawl_date)).limit(limit).all()

    @staticmethod
    def get_hotspots_by_date(date_str):
        """根据日期获取热点"""
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return HotSpot.query.filter(
                func.date(HotSpot.crawl_date) == target_date,
                HotSpot.is_today_top == True
            ).order_by(desc(HotSpot.heat_score)).all()
        except ValueError:
            return []

    @staticmethod
    def get_hotspot_by_id(hotspot_id):
        """根据ID获取热点"""
        return HotSpot.query.get(hotspot_id)

    @staticmethod
    def delete_old_data(days=30):
        """删除指定天数前的数据"""
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = HotSpot.query.filter(HotSpot.crawl_date < cutoff_date).delete()
        db.session.commit()
        return deleted_count

    @staticmethod
    def get_statistics():
        """获取统计数据"""
        total_count = HotSpot.query.count()
        today_count = HotSpot.query.filter(
            func.date(HotSpot.crawl_date) == datetime.now().date()
        ).count()
        top10_count = HotSpot.query.filter_by(is_today_top=True).count()

        # 按来源统计
        source_stats = db.session.query(
            HotSpot.source_site,
            func.count(HotSpot.id).label('count')
        ).group_by(HotSpot.source_site).all()

        return {
            'total_count': total_count,
            'today_count': today_count,
            'top10_count': top10_count,
            'source_stats': dict(source_stats)
        }