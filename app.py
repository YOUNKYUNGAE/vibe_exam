"""
AI 기반 IT 뉴스룸 메인 애플리케이션
"""
import streamlit as st
from datetime import datetime, date
import json
import os
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="My IT Newsroom",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 모듈 import
from utils.rss_collector import RSSCollector
from utils.gemini_analyzer import GeminiAnalyzer
from utils.github_manager import GitHubManager
from utils.stats_manager import StatsManager
from pages.main_page import show_main_page
from pages.dashboard_page import show_dashboard_page

# 데이터 폴더 경로
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def init_session_state():
    """세션 상태 초기화"""
    if 'rss_collector' not in st.session_state:
        st.session_state.rss_collector = RSSCollector()
    if 'gemini_analyzer' not in st.session_state:
        st.session_state.gemini_analyzer = GeminiAnalyzer()
    if 'github_manager' not in st.session_state:
        st.session_state.github_manager = GitHubManager()
    if 'stats_manager' not in st.session_state:
        st.session_state.stats_manager = StatsManager()

def main():
    """메인 함수"""
    init_session_state()
    
    # 방문자 통계 업데이트
    st.session_state.stats_manager.increment_visitor()
    
    # 사이드바 메뉴
    st.sidebar.title("📰 My IT Newsroom")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "메뉴 선택",
        ["🏠 메인 뉴스룸", "⚙️ 관리자 대시보드"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ 정보")
    st.sidebar.markdown("AI 기반 IT 뉴스 브리핑 서비스")
    
    # 페이지 라우팅
    if page == "🏠 메인 뉴스룸":
        show_main_page()
    elif page == "⚙️ 관리자 대시보드":
        show_dashboard_page()

if __name__ == "__main__":
    main()
