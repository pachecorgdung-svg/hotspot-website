from datetime import datetime, timedelta
import math

class HotSpotScorer:
    """热点评分器"""

    def __init__(self):
        # 网站权重配置
        self.site_weights = {
            '雨果网': 10,
            'AMZ123': 9,
            '新浪新闻': 8,
            '微博': 7,
            '知乎': 6,
            '抖音': 7,
            '小红书': 6,
            '其他': 5,
        }

        # 分类权重
        self.category_weights = {
            '平台动态': 9,
            '政策法规': 8,
            '资本动态': 9,
            '行业趋势': 8,
            '社交电商': 7,
            '物流仓储': 6,
            '金融财经': 7,
            '经验分享': 6,
            '行业讨论': 7,
            '社交话题': 6,
            '跨境电商': 5,
        }

    def calculate_score(self, hotspot):
        """计算热点综合分数"""
        score = 0

        # 1. 基础分数（爬虫已计算）
        score += hotspot.get('heat_score', 0)

        # 2. 网站权重
        site = hotspot.get('source_site', '其他')
        score += self.site_weights.get(site, 5)

        # 3. 分类权重
        category = hotspot.get('category', '跨境电商')
        score += self.category_weights.get(category, 5)

        # 4. 时间衰减（越新分数越高）
        publish_date = hotspot.get('publish_date')
        if isinstance(publish_date, datetime):
            hours_old = (datetime.now() - publish_date).total_seconds() / 3600
            # 72小时内有效，超过72小时分数衰减
            if hours_old <= 72:
                time_decay = max(0, 10 - (hours_old / 7.2))  # 72小时从10衰减到0
                score += time_decay
            else:
                score -= 5  # 超过72小时扣分

        # 5. 互动数据加权
        view_count = hotspot.get('view_count', 0)
        like_count = hotspot.get('like_count', 0)
        comment_count = hotspot.get('comment_count', 0)

        # 浏览量加分（对数缩放，避免过大）
        if view_count > 0:
            score += math.log10(view_count + 1) * 2

        # 点赞量加分
        score += like_count * 0.1

        # 评论量加分（评论比点赞更有价值）
        score += comment_count * 0.2

        # 6. 内容质量加分
        title = hotspot.get('title', '')
        summary = hotspot.get('summary', '')
        content = hotspot.get('content', '')

        # 标题长度适中
        title_len = len(title)
        if 15 <= title_len <= 40:
            score += 3
        elif 10 <= title_len <= 50:
            score += 2

        # 有摘要加分
        if summary and len(summary) > 20:
            score += 2

        # 有完整内容加分
        if content and len(content) > 100:
            score += 3

        # 7. 有图片加分
        if hotspot.get('image_url'):
            score += 2

        # 确保分数非负
        return max(0, score)

    def rank_hotspots(self, hotspots):
        """对热点进行排序并选择Top10"""
        if not hotspots:
            return []

        # 计算每个热点的分数
        scored_hotspots = []
        for hotspot in hotspots:
            score = self.calculate_score(hotspot)
            hotspot['final_score'] = score
            scored_hotspots.append(hotspot)

        # 按分数降序排序
        sorted_hotspots = sorted(scored_hotspots, key=lambda x: x['final_score'], reverse=True)

        # 选择Top10
        top10 = sorted_hotspots[:10]

        # 为Top10添加排名
        for i, hotspot in enumerate(top10):
            hotspot['rank'] = i + 1

        return top10

    def filter_duplicates(self, hotspots):
        """过滤重复热点（基于标题相似度）"""
        if not hotspots:
            return []

        # 简单的标题去重
        seen_titles = set()
        unique_hotspots = []

        for hotspot in hotspots:
            title = hotspot.get('title', '').strip()
            if not title:
                continue

            # 归一化标题（去除标点、转小写）
            normalized = ''.join(c for c in title if c.isalnum()).lower()

            # 检查是否已存在类似标题（简单字符串包含检查）
            is_duplicate = False
            for seen in seen_titles:
                if normalized in seen or seen in normalized:
                    is_duplicate = True
                    break

            if not is_duplicate:
                seen_titles.add(normalized)
                unique_hotspots.append(hotspot)

        return unique_hotspots

    def analyze_trends(self, hotspots):
        """分析热点趋势"""
        if not hotspots:
            return {}

        # 按分类统计
        category_counts = {}
        site_counts = {}
        tag_counts = {}

        for hotspot in hotspots:
            # 分类统计
            category = hotspot.get('category', '其他')
            category_counts[category] = category_counts.get(category, 0) + 1

            # 来源统计
            site = hotspot.get('source_site', '其他')
            site_counts[site] = site_counts.get(site, 0) + 1

            # 标签统计
            tags_str = hotspot.get('tags', '')
            if tags_str:
                tags = [tag.strip() for tag in tags_str.split(',')]
                for tag in tags:
                    if tag:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 找出热门分类和标签
        top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_sites = sorted(site_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            'total_count': len(hotspots),
            'top_categories': top_categories,
            'top_sites': top_sites,
            'top_tags': top_tags,
        }