from datetime import datetime, timedelta
import random
from .base_crawler import BaseCrawler

class NewsCrawler(BaseCrawler):
    """新闻网站爬虫（模拟版本）"""

    def __init__(self):
        super().__init__()
        self.name = "新浪新闻"
        self.base_url = "https://news.sina.com.cn"

    def crawl(self):
        """爬取新闻网站热点（模拟数据）"""
        print(f"开始爬取 {self.name}...")

        hotspots = []

        # 模拟一些跨境电商相关新闻
        sample_hotspots = [
            {
                'title': '跨境电商综试区再扩容，新增27个城市',
                'summary': '国务院批准新增27个跨境电商综合试验区，推动跨境电商高质量发展。',
                'content': '近日国务院常务会议决定...',
                'url': 'https://news.sina.com.cn/c/2024-03-04/doc-123456.shtml',
                'image_url': 'https://example.com/images/test-area.jpg',
                'publish_date': datetime.now() - timedelta(hours=3),
                'category': '政策解读',
                'tags': '综试区,政策,扩容',
                'view_count': random.randint(10000, 50000),
                'like_count': random.randint(300, 1500),
                'comment_count': random.randint(200, 800),
            },
            {
                'title': '人民币汇率波动，跨境电商企业如何应对',
                'summary': '近期人民币汇率出现波动，跨境电商企业面临汇兑风险，专家建议多种方式对冲。',
                'content': '受国际金融市场影响...',
                'url': 'https://news.sina.com.cn/c/2024-03-04/doc-123457.shtml',
                'image_url': 'https://example.com/images/exchange-rate.jpg',
                'publish_date': datetime.now() - timedelta(hours=8),
                'category': '金融财经',
                'tags': '汇率,金融,风险',
                'view_count': random.randint(8000, 40000),
                'like_count': random.randint(200, 1000),
                'comment_count': random.randint(150, 600),
            },
            {
                'title': '海外仓建设加速，跨境电商物流时效提升',
                'summary': '我国跨境电商海外仓数量快速增长，物流时效从平均15天缩短至5天以内。',
                'content': '随着跨境电商快速发展...',
                'url': 'https://news.sina.com.cn/c/2024-03-03/doc-123458.shtml',
                'image_url': 'https://example.com/images/overseas-warehouse.jpg',
                'publish_date': datetime.now() - timedelta(days=1),
                'category': '物流仓储',
                'tags': '海外仓,物流,时效',
                'view_count': random.randint(6000, 30000),
                'like_count': random.randint(150, 700),
                'comment_count': random.randint(100, 400),
            },
            {
                'title': '数字贸易成为外贸新增长点',
                'summary': '数字贸易快速发展，成为我国外贸增长新引擎，跨境电商是重要组成部分。',
                'content': '商务部数据显示...',
                'url': 'https://news.sina.com.cn/c/2024-03-02/doc-123459.shtml',
                'image_url': 'https://example.com/images/digital-trade.jpg',
                'publish_date': datetime.now() - timedelta(days=2),
                'category': '行业趋势',
                'tags': '数字贸易,外贸,增长',
                'view_count': random.randint(5000, 25000),
                'like_count': random.randint(100, 500),
                'comment_count': random.randint(80, 300),
            },
        ]

        for item in sample_hotspots:
            hotspot_data = self.parse_to_hotspot(item)
            hotspots.append(hotspot_data)

        print(f"从 {self.name} 爬取到 {len(hotspots)} 个热点")
        return hotspots