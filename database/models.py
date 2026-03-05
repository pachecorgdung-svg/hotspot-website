from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HotSpot(db.Model):
    """热点事件模型"""
    __tablename__ = 'hot_spots'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)  # 标题
    summary = db.Column(db.Text)  # 摘要
    content = db.Column(db.Text)  # 完整内容
    source_site = db.Column(db.String(100), nullable=False)  # 来源网站
    source_url = db.Column(db.String(500), nullable=False)  # 来源链接
    image_url = db.Column(db.String(500))  # 图片链接
    publish_date = db.Column(db.DateTime)  # 发布时间
    crawl_date = db.Column(db.DateTime, default=datetime.now)  # 爬取时间
    heat_score = db.Column(db.Float, default=0.0)  # 热度分数
    category = db.Column(db.String(50))  # 分类
    tags = db.Column(db.String(500))  # 标签，用逗号分隔
    view_count = db.Column(db.Integer, default=0)  # 浏览量
    like_count = db.Column(db.Integer, default=0)  # 点赞量
    comment_count = db.Column(db.Integer, default=0)  # 评论量
    is_today_top = db.Column(db.Boolean, default=False)  # 是否为今日Top10
    created_at = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'content': self.content,
            'source_site': self.source_site,
            'source_url': self.source_url,
            'image_url': self.image_url,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None,
            'crawl_date': self.crawl_date.isoformat() if self.crawl_date else None,
            'heat_score': self.heat_score,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'is_today_top': self.is_today_top,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<HotSpot {self.id}: {self.title[:50]}...>'