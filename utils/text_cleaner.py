import re
import html

class TextCleaner:
    """文本清洗工具"""

    @staticmethod
    def clean_html(text):
        """清洗HTML标签"""
        if not text:
            return ""

        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)

        # 解码HTML实体
        text = html.unescape(text)

        return text

    @staticmethod
    def remove_special_chars(text):
        """去除特殊字符"""
        if not text:
            return ""

        # 去除控制字符
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)

        # 去除多余的空白字符
        text = re.sub(r'[\r\n\t]+', ' ', text)

        # 去除多余空格
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    @staticmethod
    def clean_text(text):
        """完整文本清洗"""
        if not text:
            return ""

        text = TextCleaner.clean_html(text)
        text = TextCleaner.remove_special_chars(text)

        return text

    @staticmethod
    def extract_summary(text, max_length=200):
        """提取摘要"""
        if not text:
            return ""

        # 清洗文本
        clean_text = TextCleaner.clean_text(text)

        # 截取指定长度
        if len(clean_text) <= max_length:
            return clean_text

        # 寻找合适的截断点（句子结束）
        truncated = clean_text[:max_length]

        # 向后寻找句子结束点
        sentence_endings = ['.', '!', '?', '。', '！', '？', ';', '；']
        for i in range(max_length - 1, max_length - 50, -1):
            if i < 0:
                break
            if truncated[i] in sentence_endings:
                return truncated[:i+1]

        # 向前寻找句子结束点
        for i in range(max_length - 1, max_length - 50, -1):
            if i < 0:
                break
            if truncated[i] in [' ', ',', '，', '、']:
                return truncated[:i] + '...'

        return truncated + '...'

    @staticmethod
    def normalize_title(title):
        """规范化标题"""
        if not title:
            return ""

        # 去除首尾空白
        title = title.strip()

        # 去除标题中常见的广告标记
        ad_keywords = ['广告', '推广', '赞助', 'ADVERTISEMENT', 'SPONSORED']
        for keyword in ad_keywords:
            if keyword in title:
                title = title.replace(keyword, '')

        # 去除多余空格
        title = re.sub(r'\s+', ' ', title).strip()

        return title

    @staticmethod
    def extract_tags(text, max_tags=5):
        """从文本中提取关键词作为标签"""
        if not text:
            return []

        # 中文关键词（跨境电商相关）
        keywords = [
            '亚马逊', 'eBay', '速卖通', 'Shopify', '独立站', 'TikTok', '社交电商',
            '物流', '海外仓', '关税', '增值税', '报关', '清关', '供应链',
            '品牌', '营销', 'SEO', '广告', '引流', '转化率', '复购率',
            '支付', '汇率', '融资', '投资', 'IPO', '上市', '并购',
            '政策', '法规', '合规', '知识产权', '专利', '商标', '版权',
            '数据', '分析', '趋势', '市场', '竞争', '蓝海', '红海',
            '创新', '技术', 'AI', '大数据', '区块链', '元宇宙',
        ]

        # 查找关键词
        found_tags = []
        for keyword in keywords:
            if keyword in text:
                found_tags.append(keyword)
                if len(found_tags) >= max_tags:
                    break

        return found_tags