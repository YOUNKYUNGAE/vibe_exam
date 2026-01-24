# My IT Newsroom 📰

AI 기반 IT 뉴스 브리핑 앱 - Gemini API를 활용한 일일 IT 뉴스 요약 서비스

## 🚀 기능

- **RSS 피드 수집**: 국내 IT 미디어의 RSS 피드에서 최신 뉴스 수집
- **AI 분석**: Google Gemini API를 사용한 뉴스 요약 및 카테고리 분류
- **1페이지 브리핑**: 날짜별로 요약된 뉴스룸 제공
- **GitHub 저장**: JSON 파일을 GitHub 리포지토리에 영구 저장
- **방문자 통계**: 일별 방문자 수 추적

## 📋 요구사항

- Python 3.8+
- Streamlit
- Google Gemini API Key
- GitHub Personal Access Token (선택사항)

## 🛠️ 설치

1. 저장소 클론
```bash
git clone <repository-url>
cd cursor_test
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. Streamlit Secrets 설정

`.streamlit/secrets.toml` 파일 생성 (로컬 개발용):
```toml
GEMINI_API_KEY = "your-gemini-api-key"
GITHUB_TOKEN = "your-github-token"
GITHUB_REPO = "username/repository-name"
```

Streamlit Cloud 배포 시:
- Streamlit Cloud 대시보드에서 Secrets 설정에 위 값들을 추가

## 🎯 사용 방법

1. 앱 실행
```bash
streamlit run app.py
```

2. 관리자 대시보드에서:
   - RSS 피드 추가
   - "수집 시작" 버튼으로 뉴스 수집
   - "AI 브리핑 생성" 버튼으로 분석 및 저장

3. 메인 뉴스룸에서:
   - 날짜 선택하여 해당 날짜의 브리핑 확인

## 📁 프로젝트 구조

```
cursor_test/
├── app.py                 # 메인 애플리케이션
├── requirements.txt       # 의존성 패키지
├── pages/                 # 페이지 모듈
│   ├── main_page.py      # 메인 뉴스룸 페이지
│   └── dashboard_page.py # 관리자 대시보드
├── utils/                 # 유틸리티 모듈
│   ├── rss_collector.py  # RSS 수집
│   ├── gemini_analyzer.py # AI 분석
│   ├── github_manager.py # GitHub 저장
│   └── stats_manager.py  # 통계 관리
└── data/                  # 데이터 파일 (JSON)
    ├── feeds.json        # RSS 피드 목록
    ├── news_data.json    # 뉴스 데이터
    └── stats.json        # 방문자 통계
```

## 🔧 설정

### Gemini API Key 발급
1. [Google AI Studio](https://makersuite.google.com/app/apikey)에서 API 키 발급
2. Secrets에 `GEMINI_API_KEY`로 등록

### GitHub Token 발급
1. GitHub Settings > Developer settings > Personal access tokens
2. `repo` 권한 부여
3. Secrets에 `GITHUB_TOKEN`으로 등록
4. `GITHUB_REPO`에 저장소 이름 (예: `username/repo-name`) 설정

## 📝 라이선스

MIT License
