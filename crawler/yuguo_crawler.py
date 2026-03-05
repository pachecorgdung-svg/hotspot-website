from datetime import datetime, timedelta
import random
from .base_crawler import BaseCrawler

class YuguoCrawler(BaseCrawler):
    """雨果网爬虫（模拟版本）"""

    def __init__(self):
        super().__init__()
        self.name = "雨果网"
        self.base_url = "https://www.cifnews.com"

    def crawl(self):
        """爬取雨果网热点（模拟数据）"""
        print(f"开始爬取 {self.name}...")

        # 模拟数据 - 实际项目中应解析真实网页
        hotspots = []

        # 模拟一些跨境电商热点
        sample_hotspots = [
            {
                'title': '亚马逊2024年Prime Day日期公布，卖家需提前备战',
                'summary': '亚马逊官方公布2024年Prime Day大促日期，预计将带来新一轮销售高峰，跨境电商卖家需提前规划库存和营销策略。',
                'content': '亚马逊近日正式公布2024年Prime Day活动日期...',
                'url': 'https://www.cifnews.com/article/12345',
                'image_url': 'https://example.com/images/prime-day.jpg',
                'publish_date': datetime.now() - timedelta(hours=2),
                'category': '平台动态',
                'tags': '亚马逊,Prime Day,大促',
                'view_count': random.randint(5000, 20000),
                'like_count': random.randint(100, 500),
                'comment_count': random.randint(50, 200),
            },
            {
                'title': 'TikTok Shop美国站全面开放，中国卖家迎来新机遇',
                'summary': 'TikTok Shop美国站向中国卖家全面开放，短视频直播带货模式或将成为跨境电商新风口。',
                'content': 'TikTok Shop美国站近日宣布向中国跨境卖家全面开放...',
                'url': 'https://www.cifnews.com/article/12346',
                'image_url': 'https://example.com/images/tiktok-shop.jpg',
                'publish_date': datetime.now() - timedelta(hours=5),
                'category': '社交电商',
                'tags': 'TikTok,社交电商,美国市场',
                'view_count': random.randint(8000, 25000),
                'like_count': random.randint(200, 800),
                'comment_count': random.randint(100, 300),
            },
            {
                'title': '欧盟新电商增值税法规即将实施，卖家需及时调整',
                'summary': '欧盟新的电商增值税法规将于下月实施，对跨境卖家税务合规提出更高要求。',
                'content': '欧盟委员会近日宣布新的电商增值税法规...',
                'url': 'https://www.cifnews.com/article/12347',
                'image_url': 'https://example.com/images/eu-vat.jpg',
                'publish_date': datetime.now() - timedelta(days=1),
                'category': '政策法规',
                'tags': '欧盟,增值税,税务合规',
                'view_count': random.randint(3000, 15000),
                'like_count': random.randint(50, 300),
                'comment_count': random.randint(30, 150),
            },
            {
                'title': 'Shein计划在美国上市，估值或达900亿美元',
                'summary': '中国快时尚跨境电商Shein计划在美国进行IPO，估值可能达到900亿美元，成为年度最大科技IPO之一。',
                'content': '据知情人士透露，中国快时尚跨境电商Shein正在筹备在美国上市...',
                'url': 'https://www.cifnews.com/article/12348',
                'image_url': 'https://example.com/images/shein-ipo.jpg',
                'publish_date': datetime.now() - timedelta(days=2),
                'category': '资本动态',
                'tags': 'Shein,IPO,资本',
                'view_count': random.randint(10000, 50000),
                'like_count': random.randint(500, 2000),
                'comment_count': random.randint(300, 1000),
            },
            {
                'title': '跨境物流价格战再起，海运价格跌破成本线',
                'summary': '跨境物流市场竞争激烈，海运价格持续下跌，部分航线价格已跌破成本线。',
                'content': '近期跨境物流市场出现价格战...',
                'url': 'https://www.cifnews.com/article/12349',
                'image_url': 'https://example.com/images/shipping-price.jpg',
                'publish_date': datetime.now() - timedelta(days=3),
                'category': '物流仓储',
                'tags': '物流,海运,价格战',
                'view_count': random.randint(4000, 18000),
                'like_count': random.randint(80, 400),
                'comment_count': random.randint(40, 200),
            },
        ]

        for item in sample_hotspots:
            hotspot_data = self.parse_to_hotspot(item)
            hotspots.append(hotspot_data)

        print(f"从 {self.name} 爬取到 {len(hotspots)} 个热点")
        return hotspots