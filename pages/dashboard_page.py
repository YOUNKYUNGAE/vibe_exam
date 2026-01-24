"""
관리자 대시보드 페이지
"""
import streamlit as st
from datetime import datetime
import json
from pathlib import Path
import pandas as pd

def show_dashboard_page():
    """관리자 대시보드 페이지 표시"""
    st.title("⚙️ 관리자 대시보드")
    st.markdown("---")
    
    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["📡 RSS 피드 관리", "🔄 데이터 수집 및 분석", "📊 방문자 통계"])
    
    with tab1:
        show_feed_management()
    
    with tab2:
        show_data_collection()
    
    with tab3:
        show_visitor_stats()

def show_feed_management():
    """RSS 피드 관리 섹션"""
    st.header("📡 RSS 피드 관리")
    
    # 피드 로드
    feeds_data = load_feeds()
    feeds = feeds_data.get('feeds', [])
    
    # 피드 리스트 표시
    st.subheader("등록된 피드 목록")
    
    if feeds:
        for idx, feed in enumerate(feeds):
            with st.expander(f"{feed.get('name', 'Unknown')} - {feed.get('url', '')}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"이름: {feed.get('name', '')}")
                    st.text(f"URL: {feed.get('url', '')}")
                    st.text(f"상태: {'활성' if feed.get('enabled', True) else '비활성'}")
                with col2:
                    if st.button("삭제", key=f"delete_{idx}"):
                        feeds.pop(idx)
                        save_feeds({'feeds': feeds})
                        st.success("피드가 삭제되었습니다.")
                        st.rerun()
    else:
        st.info("등록된 피드가 없습니다.")
    
    st.markdown("---")
    
    # 새 피드 추가
    st.subheader("새 피드 추가")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_feed_name = st.text_input("피드 이름", key="new_feed_name")
    with col2:
        new_feed_url = st.text_input("RSS URL", key="new_feed_url")
    
    if st.button("피드 추가"):
        if new_feed_name and new_feed_url:
            new_feed = {
                "name": new_feed_name,
                "url": new_feed_url,
                "enabled": True,
                "added_at": datetime.now().isoformat()
            }
            feeds.append(new_feed)
            save_feeds({'feeds': feeds})
            st.success(f"'{new_feed_name}' 피드가 추가되었습니다.")
            st.rerun()
        else:
            st.error("피드 이름과 URL을 모두 입력해주세요.")

def show_data_collection():
    """데이터 수집 및 분석 섹션"""
    st.header("🔄 데이터 수집 및 AI 분석")
    
    # RSS 수집
    st.subheader("1. RSS 피드 수집")
    
    if st.button("📥 수집 시작", type="primary"):
        with st.spinner("RSS 피드를 수집하는 중..."):
            feeds_data = load_feeds()
            feed_urls = [f['url'] for f in feeds_data.get('feeds', []) if f.get('enabled', True)]
            
            if not feed_urls:
                st.error("등록된 활성 피드가 없습니다. 먼저 RSS 피드를 추가해주세요.")
            else:
                result = st.session_state.rss_collector.collect_articles(feed_urls, max_articles=50)
                
                if result['articles']:
                    st.session_state.collected_articles = result['articles']
                    st.success(f"✅ {result['total_count']}개의 기사를 수집했습니다.")
                    
                    if result['failed_feeds']:
                        st.warning(f"⚠️ {len(result['failed_feeds'])}개의 피드 수집에 실패했습니다.")
                        for failed in result['failed_feeds']:
                            st.text(f"- {failed['url']}: {failed['error']}")
                else:
                    st.error("수집된 기사가 없습니다.")
    
    st.markdown("---")
    
    # AI 분석
    st.subheader("2. AI 브리핑 생성")
    
    if 'collected_articles' in st.session_state and st.session_state.collected_articles:
        st.info(f"📰 {len(st.session_state.collected_articles)}개의 기사가 준비되었습니다.")
        
        if st.button("🤖 AI 브리핑 생성", type="primary"):
            with st.spinner("AI가 뉴스를 분석하는 중... (시간이 걸릴 수 있습니다)"):
                result = st.session_state.gemini_analyzer.analyze_news(
                    st.session_state.collected_articles
                )
                
                if result.get('success'):
                    # 오늘 날짜로 저장
                    today = datetime.now().date().isoformat()
                    
                    # 기존 데이터 로드
                    news_data = load_news_data()
                    news_data[today] = {
                        'summary': result.get('summary', ''),
                        'sections': result.get('sections', []),
                        'sources': result.get('sources', []),
                        'article_count': result.get('article_count', 0),
                        'created_at': result.get('created_at', datetime.now().isoformat())
                    }
                    
                    # GitHub에 저장
                    save_result = st.session_state.github_manager.save_json_file(
                        "news_data.json",
                        news_data,
                        f"Update news data for {today}"
                    )
                    
                    if save_result.get('success'):
                        st.success("✅ AI 브리핑이 생성되고 저장되었습니다!")
                        if save_result.get('local_only'):
                            st.info("ℹ️ 로컬에만 저장되었습니다. (GitHub 설정 필요)")
                    else:
                        st.error(f"저장 실패: {save_result.get('error', '알 수 없는 오류')}")
                else:
                    st.error(f"❌ AI 분석 실패: {result.get('error', '알 수 없는 오류')}")
    else:
        st.info("먼저 '수집 시작' 버튼을 눌러 기사를 수집해주세요.")

def show_visitor_stats():
    """방문자 통계 섹션"""
    st.header("📊 방문자 통계")
    
    stats = st.session_state.stats_manager.get_visitor_data()
    
    # 총 방문자 수
    total = stats.get('total_visitors', 0)
    st.metric("총 방문자 수", f"{total:,}명")
    
    st.markdown("---")
    
    # 일별 방문자 그래프
    daily_visitors = stats.get('visitors', {})
    
    if daily_visitors:
        # 데이터프레임 생성
        df = pd.DataFrame([
            {'날짜': date, '방문자 수': count}
            for date, count in sorted(daily_visitors.items())
        ])
        
        # 그래프 표시
        st.subheader("일별 방문자 추이")
        st.line_chart(df.set_index('날짜'))
        
        # 테이블 표시
        st.subheader("상세 통계")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("아직 방문자 통계 데이터가 없습니다.")

def load_feeds() -> dict:
    """피드 데이터 로드"""
    try:
        if st.session_state.github_manager.client_initialized:
            data = st.session_state.github_manager.load_json_file("feeds.json")
            if data:
                return data
        
        data_path = Path("data/feeds.json")
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"피드 데이터 로드 실패: {e}")
    
    return {'feeds': []}

def save_feeds(feeds_data: dict):
    """피드 데이터 저장"""
    try:
        save_result = st.session_state.github_manager.save_json_file(
            "feeds.json",
            feeds_data,
            "Update RSS feeds"
        )
        
        if not save_result.get('success'):
            st.error(f"저장 실패: {save_result.get('error', '알 수 없는 오류')}")
    except Exception as e:
        st.error(f"저장 중 오류 발생: {e}")

def load_news_data() -> dict:
    """뉴스 데이터 로드"""
    try:
        if st.session_state.github_manager.client_initialized:
            data = st.session_state.github_manager.load_json_file("news_data.json")
            if data:
                return data
        
        data_path = Path("data/news_data.json")
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"뉴스 데이터 로드 실패: {e}")
    
    return {}
