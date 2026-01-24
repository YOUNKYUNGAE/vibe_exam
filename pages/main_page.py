"""
메인 뉴스룸 페이지
"""
import streamlit as st
from datetime import date, datetime
import json
from pathlib import Path

def show_main_page():
    """메인 뉴스룸 페이지 표시"""
    st.title("📰 My IT Newsroom")
    st.markdown("---")
    
    # 날짜 선택
    selected_date = st.date_input(
        "📅 날짜 선택",
        value=date.today(),
        max_value=date.today()
    )
    
    # 데이터 로드
    news_data = load_news_data()
    
    # 선택한 날짜의 데이터 표시
    date_key = selected_date.isoformat()
    
    if date_key in news_data:
        display_news_briefing(news_data[date_key])
    else:
        st.info(f"📭 {selected_date.strftime('%Y년 %m월 %d일')}의 뉴스 브리핑이 아직 생성되지 않았습니다.")
        st.markdown("관리자 대시보드에서 뉴스를 수집하고 AI 브리핑을 생성해주세요.")

def load_news_data():
    """뉴스 데이터 로드"""
    try:
        # GitHub에서 로드 시도
        if st.session_state.github_manager.client_initialized:
            data = st.session_state.github_manager.load_json_file("news_data.json")
            if data:
                return data
        
        # 로컬에서 로드
        data_path = Path("data/news_data.json")
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
    
    return {}

def display_news_briefing(briefing_data):
    """뉴스 브리핑 표시"""
    # 헤드라인
    st.markdown("### 🌟 오늘의 핵심 IT 트렌드")
    st.markdown(f"**{briefing_data.get('summary', '요약이 없습니다.')}**")
    st.markdown("---")
    
    # 카테고리별 섹션
    sections = briefing_data.get('sections', [])
    if sections:
        st.markdown("### 📑 카테고리별 요약")
        
        # 2열 레이아웃
        cols = st.columns(2)
        
        for idx, section in enumerate(sections):
            col = cols[idx % 2]
            
            with col:
                category = section.get('category', '기타')
                content = section.get('content', '')
                
                # 카테고리별 이모지
                emoji_map = {
                    'AI/반도체': '🤖',
                    'SW/보안': '🔒',
                    '플랫폼/기타': '🌐',
                    'AI': '🤖',
                    '반도체': '💻',
                    '보안': '🔒',
                    'SW': '💾'
                }
                emoji = emoji_map.get(category, '📰')
                
                st.markdown(f"#### {emoji} {category}")
                st.markdown(content)
                st.markdown("")
    
    # 원문 소스
    sources = briefing_data.get('sources', [])
    if sources:
        st.markdown("---")
        st.markdown("### 🔗 원문 링크")
        
        for source in sources:
            title = source.get('title', '제목 없음')
            url = source.get('url', '')
            source_name = source.get('source', '')
            
            if url:
                st.markdown(f"- [{title}]({url}) {f'({source_name})' if source_name else ''}")
            else:
                st.markdown(f"- {title} {f'({source_name})' if source_name else ''}")
    
    # 메타 정보
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        article_count = briefing_data.get('article_count', 0)
        st.caption(f"📊 분석 기사 수: {article_count}개")
    with col2:
        created_at = briefing_data.get('created_at', '')
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                st.caption(f"🕐 생성 시간: {dt.strftime('%Y-%m-%d %H:%M')}")
            except:
                st.caption(f"🕐 생성 시간: {created_at}")
