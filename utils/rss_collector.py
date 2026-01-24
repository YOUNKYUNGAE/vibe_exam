"""
RSS 피드 수집 모듈
"""
import feedparser
import requests
from datetime import datetime
from typing import List, Dict
import time
import logging

logger = logging.getLogger(__name__)

class RSSCollector:
    """RSS 피드를 수집하고 파싱하는 클래스"""
    
    def __init__(self):
        self.timeout = 10
        self.max_retries = 3
        self.retry_delay = 2
    
    def fetch_feed(self, url: str) -> Dict:
        """
        RSS 피드를 가져옵니다.
        
        Args:
            url: RSS 피드 URL
            
        Returns:
            파싱된 피드 데이터 딕셔너리
        """
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # feedparser로 파싱
                feed = feedparser.parse(response.content)
                
                if feed.bozo and feed.bozo_exception:
                    logger.warning(f"피드 파싱 경고: {url} - {feed.bozo_exception}")
                
                return {
                    'success': True,
                    'feed': feed,
                    'url': url
                }
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"피드 접근 실패 (시도 {attempt + 1}/{self.max_retries}): {url} - {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    return {
                        'success': False,
                        'error': str(e),
                        'url': url
                    }
            except Exception as e:
                logger.error(f"예상치 못한 오류: {url} - {e}")
                return {
                    'success': False,
                    'error': str(e),
                    'url': url
                }
        
        return {
            'success': False,
            'error': '최대 재시도 횟수 초과',
            'url': url
        }
    
    def collect_articles(self, feed_urls: List[str], max_articles: int = 50) -> Dict:
        """
        여러 RSS 피드에서 기사를 수집합니다.
        
        Args:
            feed_urls: RSS 피드 URL 리스트
            max_articles: 최대 수집 기사 수
            
        Returns:
            수집된 기사 데이터
        """
        all_articles = []
        failed_feeds = []
        
        for url in feed_urls:
            result = self.fetch_feed(url)
            
            if not result['success']:
                failed_feeds.append({
                    'url': url,
                    'error': result.get('error', '알 수 없는 오류')
                })
                continue
            
            feed = result['feed']
            
            # 피드 정보 추출
            feed_title = feed.feed.get('title', 'Unknown')
            
            # 기사 항목 추출
            for entry in feed.entries:
                if len(all_articles) >= max_articles:
                    break
                
                article = {
                    'title': entry.get('title', '제목 없음'),
                    'link': entry.get('link', ''),
                    'published': self._parse_date(entry.get('published', '')),
                    'summary': entry.get('summary', entry.get('description', '')),
                    'source': feed_title,
                    'source_url': url
                }
                
                all_articles.append(article)
            
            # 크롤링 간격 (5분 간격 권장)
            time.sleep(1)
        
        return {
            'articles': all_articles,
            'total_count': len(all_articles),
            'failed_feeds': failed_feeds
        }
    
    def _parse_date(self, date_str: str) -> str:
        """날짜 문자열을 ISO 형식으로 변환"""
        if not date_str:
            return datetime.now().isoformat()
        
        try:
            # feedparser의 published_parsed 사용
            from dateutil import parser
            dt = parser.parse(date_str)
            return dt.isoformat()
        except:
            return datetime.now().isoformat()
