from datetime import datetime
from .yuguo_crawler import YuguoCrawler
from .news_crawler import NewsCrawler
from .social_crawler import SocialCrawler
from utils import HotSpotScorer, TextCleaner
from database.db_manager import DBManager

class CrawlerManager:
    """爬虫管理器"""

    def __init__(self):
        self.crawlers = [YuguoCrawler(), NewsCrawler(), SocialCrawler()]
        self.scorer = HotSpotScorer()

    def run_all(self):
        """运行所有爬虫并处理数据"""
        all_hotspots = []

        # 运行每个爬虫
        for crawler in self.crawlers:
            try:
                hotspots = crawler.crawl()
                all_hotspots.extend(hotspots)
                print(f"{crawler.name} 爬取完成，获得 {len(hotspots)} 个热点")
            except Exception as e:
                print(f"{crawler.name} 爬取失败: {e}")

        # 去重
        unique_hotspots = self.scorer.filter_duplicates(all_hotspots)
        print(f"去重后剩余 {len(unique_hotspots)} 个热点")

        # 计算分数并排序
        ranked_hotspots = self.scorer.rank_hotspots(unique_hotspots)
        print(f"排序后得到 {len(ranked_hotspots)} 个热点")

        # 保存到数据库
        hotspot_ids = []
        for i, hotspot in enumerate(ranked_hotspots[:10]):  # 只保存Top10
            try:
                # 清理数据
                hotspot['title'] = TextCleaner.normalize_title(hotspot.get('title', ''))
                hotspot['summary'] = TextCleaner.extract_summary(
                    hotspot.get('summary', '') or hotspot.get('content', '')
                )

                # 保存到数据库
                saved = DBManager.add_hotspot(hotspot)
                hotspot_ids.append(saved.id)

                print(f"保存热点 {i+1}: {hotspot['title'][:50]}...")
            except Exception as e:
                print(f"保存热点失败: {e}")

        # 更新今日Top10标记
        if hotspot_ids:
            DBManager.update_today_top10(hotspot_ids)
            print(f"更新今日Top10标记完成，{len(hotspot_ids)} 个热点")

        return ranked_hotspots[:10]

    def run_single(self, crawler_name):
        """运行单个爬虫"""
        for crawler in self.crawlers:
            if crawler.name == crawler_name:
                return crawler.crawl()
        return []

    def get_crawler_stats(self):
        """获取爬虫统计信息"""
        stats = {
            'total_crawlers': len(self.crawlers),
            'crawler_names': [c.name for c in self.crawlers],
            'last_run': datetime.now().isoformat()
        }
        return stats

# 全局实例
crawler_manager = CrawlerManager()