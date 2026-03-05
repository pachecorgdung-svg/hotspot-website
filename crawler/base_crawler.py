import requests
import time
import random
from abc import ABC, abstractmethod
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class BaseCrawler(ABC):
    """爬虫基类"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.base_url = None
        self.name = None

    def fetch_page(self, url, max_retries=3):
        """获取页面内容"""
        for attempt in range(max_retries):
            try:
                # 随机延迟，避免被屏蔽
                time.sleep(random.uniform(1, 3))

                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                # 检查编码
                if response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'

                return response.text
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"获取页面失败: {url}, 错误: {e}")
                    return None
                time.sleep(2 ** attempt)  # 指数退避

        return None

    def clean_text(self, text):
        """清洗文本"""
        if not text:
            return ""

        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 去除特殊字符
        text = re.sub(r'[\r\n\t]+', ' ', text)
        # 去除多余空格
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def extract_date(self, date_str):
        """提取日期时间"""
        if not date_str:
            return datetime.now()

        # 常见日期格式匹配
        date_patterns = [
            r'(\d{4})[年.-](\d{1,2})[月.-](\d{1,2})[日]?',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{4})/(\d{1,2})/(\d{1,2})',
        ]

        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                year, month, day = match.groups()
                try:
                    return datetime(int(year), int(month), int(day))
                except ValueError:
                    continue

        # 时间格式
        time_patterns = [
            r'(\d{1,2}):(\d{1,2}):(\d{1,2})',
            r'(\d{1,2}):(\d{1,2})',
        ]

        for pattern in time_patterns:
            match = re.search(pattern, date_str)
            if match:
                # 使用当前日期加上时间
                now = datetime.now()
                groups = match.groups()
                if len(groups) >= 2:
                    try:
                        hour, minute = int(groups[0]), int(groups[1])
                        return datetime(now.year, now.month, now.day, hour, minute)
                    except ValueError:
                        continue

        return datetime.now()

    def calculate_heat_score(self, item):
        """计算热度分数（子类可重写）"""
        # 基础分数
        score = 0

        # 标题长度适中加分
        title_len = len(item.get('title', ''))
        if 10 <= title_len <= 50:
            score += 5

        # 有摘要加分
        if item.get('summary'):
            score += 3

        # 有图片加分
        if item.get('image_url'):
            score += 2

        # 来源网站权重
        site_weights = {
            '雨果网': 10,
            'AMZ123': 9,
            '新浪新闻': 8,
            '微博': 7,
            '知乎': 6,
        }
        score += site_weights.get(item.get('source_site', ''), 5)

        return score

    @abstractmethod
    def crawl(self):
        """爬取方法（子类必须实现）"""
        pass

    def parse_to_hotspot(self, item):
        """解析为热点数据格式"""
        return {
            'title': item.get('title', ''),
            'summary': item.get('summary', ''),
            'content': item.get('content', ''),
            'source_site': self.name,
            'source_url': item.get('url', ''),
            'image_url': item.get('image_url', ''),
            'publish_date': item.get('publish_date', datetime.now()),
            'heat_score': self.calculate_heat_score(item),
            'category': item.get('category', '跨境电商'),
            'tags': item.get('tags', ''),
            'view_count': item.get('view_count', 0),
            'like_count': item.get('like_count', 0),
            'comment_count': item.get('comment_count', 0),
        }