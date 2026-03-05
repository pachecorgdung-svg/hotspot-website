from datetime import datetime, timedelta
import random
from .base_crawler import BaseCrawler

class SocialCrawler(BaseCrawler):
    """社交媒体爬虫（模拟版本）"""

    def __init__(self):
        super().__init__()
        self.name = "微博"
        self.base_url = "https://weibo.com"

    def crawl(self):
        """爬取社交媒体热点（模拟数据）"""
        print(f"开始爬取 {self.name}...")

        hotspots = []

        # 模拟一些社交媒体热点话题
        sample_hotspots = [
            {
                'title': '#跨境电商人的一天# 上热搜',
                'summary': '话题#跨境电商人的一天#登上微博热搜，网友分享跨境电商工作日常。',
                'content': '近日微博话题#跨境电商人的一天#引发热议...',
                'url': 'https://weibo.com/hashtag/跨境电商人的一天',
                'image_url': 'https://example.com/images/weibo-topic.jpg',
                'publish_date': datetime.now() - timedelta(hours=1),
                'category': '社交话题',
                'tags': '微博,热搜,日常',
                'view_count': random.randint(500000, 2000000),
                'like_count': random.randint(5000, 20000),
                'comment_count': random.randint(3000, 10000),
            },
            {
                'title': '知乎热议：跨境电商还能做吗？',
                'summary': '知乎问题"2024年跨境电商还能做吗？"引发上千回答，行业人士各抒己见。',
                'content': '知乎上一个关于跨境电商前景的问题...',
                'url': 'https://www.zhihu.com/question/123456',
                'image_url': 'https://example.com/images/zhihu-discuss.jpg',
                'publish_date': datetime.now() - timedelta(hours=4),
                'category': '行业讨论',
                'tags': '知乎,讨论,前景',
                'view_count': random.randint(100000, 500000),
                'like_count': random.randint(1000, 5000),
                'comment_count': random.randint(800, 3000),
            },
            {
                'title': '抖音电商培训课程火爆',
                'summary': '抖音上跨境电商培训课程受到追捧，相关视频播放量超千万。',
                'content': '随着跨境电商热度上升...',
                'url': 'https://www.douyin.com/video/123456',
                'image_url': 'https://example.com/images/douyin-course.jpg',
                'publish_date': datetime.now() - timedelta(days=1),
                'category': '社交电商',
                'tags': '抖音,培训,课程',
                'view_count': random.randint(1000000, 5000000),
                'like_count': random.randint(10000, 50000),
                'comment_count': random.randint(5000, 20000),
            },
            {
                'title': '小红书上国货出海经验分享',
                'summary': '小红书博主分享国货品牌出海经验，笔记获数万收藏。',
                'content': '一位小红书博主详细分享了...',
                'url': 'https://www.xiaohongshu.com/note/123456',
                'image_url': 'https://example.com/images/xhs-note.jpg',
                'publish_date': datetime.now() - timedelta(days=2),
                'category': '经验分享',
                'tags': '小红书,国货,出海',
                'view_count': random.randint(200000, 1000000),
                'like_count': random.randint(5000, 20000),
                'comment_count': random.randint(2000, 8000),
            },
        ]

        for item in sample_hotspots:
            hotspot_data = self.parse_to_hotspot(item)
            hotspots.append(hotspot_data)

        print(f"从 {self.name} 爬取到 {len(hotspots)} 个热点")
        return hotspots