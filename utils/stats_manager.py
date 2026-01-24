"""
방문자 통계 관리 모듈
"""
import json
from datetime import datetime, date
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class StatsManager:
    """방문자 통계를 관리하는 클래스"""
    
    def __init__(self, filename: str = "stats.json"):
        self.filename = filename
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.file_path = self.data_dir / filename
        self._load_stats()
    
    def _load_stats(self):
        """통계 데이터 로드"""
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
            except Exception as e:
                logger.error(f"통계 파일 로드 실패: {e}")
                self.stats = self._get_default_stats()
        else:
            self.stats = self._get_default_stats()
    
    def _get_default_stats(self):
        """기본 통계 구조 반환"""
        return {
            "visitors": {},
            "total_visitors": 0,
            "last_updated": datetime.now().isoformat()
        }
    
    def increment_visitor(self):
        """방문자 수 증가"""
        today = date.today().isoformat()
        
        if "visitors" not in self.stats:
            self.stats["visitors"] = {}
        
        if today not in self.stats["visitors"]:
            self.stats["visitors"][today] = 0
        
        self.stats["visitors"][today] += 1
        self.stats["total_visitors"] = sum(self.stats["visitors"].values())
        self.stats["last_updated"] = datetime.now().isoformat()
        
        self._save_stats()
    
    def _save_stats(self):
        """통계 데이터 저장"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"통계 파일 저장 실패: {e}")
    
    def get_visitor_data(self):
        """방문자 통계 데이터 반환"""
        return self.stats.copy()
    
    def get_daily_visitors(self):
        """일별 방문자 수 반환"""
        return self.stats.get("visitors", {})
    
    def get_total_visitors(self):
        """총 방문자 수 반환"""
        return self.stats.get("total_visitors", 0)
