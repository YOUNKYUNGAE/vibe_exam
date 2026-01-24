"""
Gemini API를 사용한 AI 분석 모듈
"""
import google.generativeai as genai
import json
import time
import logging
from typing import Dict, List
import streamlit as st

logger = logging.getLogger(__name__)

class GeminiAnalyzer:
    """Gemini API를 사용하여 뉴스를 분석하는 클래스"""
    
    def __init__(self):
        self.model_name = "gemini-1.5-flash"
        self.max_retries = 3
        self.retry_delay = 2
        self._initialize_client()
    
    def _initialize_client(self):
        """Gemini API 클라이언트 초기화"""
        try:
            # Streamlit secrets에서 API 키 가져오기
            try:
                api_key = st.secrets.get("GEMINI_API_KEY", "")
            except:
                # secrets가 없으면 환경 변수에서 시도
                import os
                api_key = os.getenv("GEMINI_API_KEY", "")
            
            if not api_key:
                logger.warning("GEMINI_API_KEY가 설정되지 않았습니다.")
                self.client_initialized = False
                return
            
            genai.configure(api_key=api_key)
            self.client_initialized = True
        except Exception as e:
            logger.error(f"Gemini API 초기화 실패: {e}")
            self.client_initialized = False
    
    def analyze_news(self, articles: List[Dict]) -> Dict:
        """
        수집된 뉴스 기사들을 AI로 분석합니다.
        
        Args:
            articles: 기사 리스트
            
        Returns:
            분석 결과 딕셔너리
        """
        if not self.client_initialized:
            return {
                'success': False,
                'error': 'Gemini API가 초기화되지 않았습니다. API 키를 확인해주세요.'
            }
        
        if not articles:
            return {
                'success': False,
                'error': '분석할 기사가 없습니다.'
            }
        
        # 기사 텍스트 준비
        articles_text = self._prepare_articles_text(articles)
        
        # 프롬프트 생성
        prompt = self._create_prompt(articles_text)
        
        # API 호출 (재시도 로직 포함)
        for attempt in range(self.max_retries):
            try:
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                
                # 응답 파싱
                result = self._parse_response(response.text, articles)
                
                return {
                    'success': True,
                    **result
                }
                
            except Exception as e:
                logger.warning(f"API 호출 실패 (시도 {attempt + 1}/{self.max_retries}): {e}")
                
                if "429" in str(e) or "quota" in str(e).lower():
                    # Rate limit 도달 시 더 긴 대기
                    wait_time = self.retry_delay * (2 ** attempt) * 5
                    logger.info(f"Rate limit 도달. {wait_time}초 대기...")
                    time.sleep(wait_time)
                else:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                    else:
                        return {
                            'success': False,
                            'error': f'API 호출 실패: {str(e)}'
                        }
        
        return {
            'success': False,
            'error': '최대 재시도 횟수 초과'
        }
    
    def _prepare_articles_text(self, articles: List[Dict]) -> str:
        """기사 리스트를 텍스트로 변환"""
        text_parts = []
        for i, article in enumerate(articles, 1):
            text_parts.append(f"[기사 {i}]")
            text_parts.append(f"제목: {article.get('title', '')}")
            text_parts.append(f"요약: {article.get('summary', '')[:500]}")
            text_parts.append("")
        
        return "\n".join(text_parts)
    
    def _create_prompt(self, articles_text: str) -> str:
        """AI 분석 프롬프트 생성"""
        prompt = f"""당신은 IT 전문 에디터입니다. 아래의 IT 뉴스 기사들을 종합하여 분석해주세요.

요청 사항:
1. 여러 뉴스 소스를 종합하여 중복된 내용을 제외하고, 비즈니스 관점에서 중요한 3가지 핵심 포인트를 도출하세요.
2. 일반 독자가 읽기 쉽게 친절한 톤으로 작성하세요.
3. 기사를 카테고리별로 분류하세요 (AI/반도체, SW/보안, 플랫폼/기타 등).

응답 형식은 반드시 다음 JSON 형식으로 작성해주세요:
{{
    "summary": "오늘의 핵심 IT 트렌드 요약 (3문장)",
    "sections": [
        {{
            "category": "카테고리명",
            "content": "해당 카테고리의 요약 내용"
        }}
    ]
}}

기사 목록:
{articles_text}

JSON 형식으로만 응답해주세요. 다른 설명은 포함하지 마세요."""
        
        return prompt
    
    def _parse_response(self, response_text: str, articles: List[Dict]) -> Dict:
        """API 응답을 파싱하여 구조화된 데이터로 변환"""
        try:
            # JSON 추출 시도
            # 응답에서 JSON 부분만 추출
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
            else:
                # JSON이 없으면 기본 구조 생성
                parsed = {
                    "summary": response_text[:500],
                    "sections": [{"category": "기타", "content": response_text}]
                }
            
            # 원문 소스 정보 추가
            sources = []
            for article in articles:
                sources.append({
                    "title": article.get('title', ''),
                    "url": article.get('link', ''),
                    "source": article.get('source', ''),
                    "published": article.get('published', '')
                })
            
            return {
                "summary": parsed.get("summary", "요약을 생성할 수 없습니다."),
                "sections": parsed.get("sections", []),
                "sources": sources,
                "article_count": len(articles),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {e}")
            # 기본 구조 반환
            return {
                "summary": response_text[:500] if response_text else "요약을 생성할 수 없습니다.",
                "sections": [{"category": "기타", "content": response_text[:1000] if response_text else ""}],
                "sources": [{"title": article.get('title', ''), "url": article.get('link', '')} for article in articles],
                "article_count": len(articles),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
