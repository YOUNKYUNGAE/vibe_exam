Cursor AI를 통해 개발할 **'AI 기반 IT 뉴스룸'**의 상세 명세서입니다. 이 명세서를 Cursor AI의 대화창(Chat)에 입력하거나 단계별로 구현을 요청할 때 참고자료로 사용하세요.

---

# [상세 명세서] AI 기반 IT 뉴스 브리핑 앱: "My IT Newsroom"

## 1. 프로젝트 개요
*   **목적**: 국내 IT 뉴스 RSS를 수집하여 Gemini API로 분석하고, 날짜별로 요약된 '1페이지 뉴스룸'을 제공.
*   **기술 스택**: 
    *   Python 3.8+
    *   Streamlit (UI 프레임워크)
    *   Google Gemini API (1.5 Flash) - AI 분석
    *   feedparser - RSS 피드 파싱
    *   requests - HTTP 요청
    *   PyGithub - GitHub API 연동
    *   GitHub (Storage) - JSON 파일 영구 저장
    *   Streamlit Cloud (Deployment) - 배포 플랫폼
*   **데이터 관리**: 별도의 DB 없이 GitHub 리포지토리 내 **JSON 파일**을 사용해 영구 저장.

## 2. 주요 기능 상세

### 2.1. 메인 화면 (뉴스 브리핑 서비스)
*   **1페이지 브리핑**: 특정 날짜를 선택하면 해당 날짜의 AI 요약 보고서를 한 페이지로 출력.
*   **콘텐츠 구성**:
    *   **Headline**: 오늘의 핵심 IT 트렌드 요약 (3문장).
    *   **Category View**: (AI가 분류한) AI/반도체, SW/보안, 플랫폼/기타 등 섹션별 요약.
    *   **Source Links**: 분석에 사용된 원문 뉴스들의 제목과 링크 리스트.
*   **UI/UX**: 
    *   깔끔한 매거진 스타일의 레이아웃 (Streamlit의 `st.container`, `st.columns` 활용)
    *   날짜 선택기: `st.date_input` 위젯 사용
    *   로딩 상태 표시: `st.spinner` 또는 `st.progress` 활용
    *   에러 메시지: `st.error` 또는 `st.warning`으로 사용자 친화적 표시
    *   섹션 구분: 이모지와 구분선으로 가독성 향상

### 2.2. 대시보드 (관리자 페이지)
*   **RSS 피드 관리**:
    *   국내 IT 미디어(예: 전자신문, ZDNet Korea, 디지털데일리 등)의 RSS URL 추가/삭제.
    *   등록된 피드 리스트 확인.
*   **데이터 수집 및 AI 분석 실행**:
    *   '수집 시작' 버튼: 등록된 RSS에서 최신 기사 크롤링.
    *   'AI 브리핑 생성' 버튼: 수집된 텍스트를 Gemini API에 전달하여 분석 후 JSON으로 저장.
*   **방문자 통계**:
    *   날짜별 접속자 수 그래프 (Line Chart).
    *   누적 방문자 수 표시 (Metric).

### 2.3. 데이터 저장 및 연동 (GitHub 저장소 활용)
*   **파일 구조**:
    *   `feeds.json`: RSS URL 목록.
    *   `news_data.json`: 날짜별 AI 분석 결과 및 원문 메타데이터.
    *   `stats.json`: 일자별 방문자 수 통계.
*   **영구 저장 로직**: 
    *   Streamlit Cloud의 휘발성 저장소 문제를 해결하기 위해, 데이터 변경 시 **GitHub API(PyGithub)**를 호출하여 JSON 파일을 리포지토리에 직접 `Commit & Push`하는 로직 포함.

---

## 3. 기술적 요구 사항

### 3.1. AI 프롬프트 엔지니어링 (Gemini API)
*   **역할 정의**: "당신은 IT 전문 에디터입니다."
*   **요청 사항**: "여러 뉴스 소스를 종합하여 중복된 내용을 제외하고, 비즈니스 관점에서 중요한 3가지 핵심 포인트를 도출하세요. 일반 독자가 읽기 쉽게 친절한 톤으로 작성하세요."

### 3.2. 보안 설정
*   **Secret 관리**: Gemini API Key와 GitHub Personal Access Token(PAT)은 소스코드에 노출하지 않고 Streamlit Cloud의 `Secrets` 설정에 보관.
*   **API 호출 제한**: 
    *   Gemini API 호출 빈도 제한 (Rate Limiting) 구현
    *   RSS 크롤링 간격 설정 (최소 5분 간격 권장)
    *   대용량 피드 처리 시 청크 단위로 분할하여 API 호출

### 3.3. 필수 라이브러리
*   `streamlit`: 웹 UI 프레임워크
*   `feedparser`: RSS/Atom 피드 파싱
*   `requests`: HTTP 요청 처리
*   `google-generativeai`: Gemini API 클라이언트
*   `PyGithub`: GitHub API 연동
*   `python-dateutil`: 날짜/시간 처리 (선택)

---

## 4. 데이터 스키마 (JSON 구조 예시)

### `news_data.json`
```json
{
  "2025-01-24": {
    "summary": "AI 모델의 경량화가 가속화되고 있으며, 국내 반도체 기업들의 실적이 반등하고 있습니다...",
    "sections": [
      {"category": "AI/반도체", "content": "삼성전자, HBM3E 양산 준비 완료..."},
      {"category": "SW/보안", "content": "국내 보안 업체들, 생성형 AI 공격 방어 솔루션 출시..."}
    ],
    "sources": [
      {"title": "뉴스 제목", "url": "https://...", "source": "전자신문", "published": "2025-01-24T09:00:00Z"}
    ],
    "created_at": "2025-01-24T10:30:00Z",
    "article_count": 15
  }
}
```

### `feeds.json`
```json
{
  "feeds": [
    {
      "name": "전자신문",
      "url": "https://www.etnews.com/rss/section/03000000.xml",
      "enabled": true,
      "added_at": "2025-01-20T00:00:00Z"
    },
    {
      "name": "ZDNet Korea",
      "url": "https://www.zdnet.co.kr/rss/all.xml",
      "enabled": true,
      "added_at": "2025-01-20T00:00:00Z"
    }
  ]
}
```

### `stats.json`
```json
{
  "visitors": {
    "2025-01-24": 42,
    "2025-01-23": 38,
    "2025-01-22": 35
  },
  "total_visitors": 115,
  "last_updated": "2025-01-24T15:30:00Z"
}
```

---

## 5. 에러 처리 및 예외 상황

### 5.1. RSS 피드 관련
*   **피드 접근 실패**: 네트워크 오류, 타임아웃, 404 에러 등
    *   재시도 로직 구현 (최대 3회)
    *   실패한 피드는 건너뛰고 나머지 피드 계속 처리
    *   사용자에게 실패한 피드 목록 표시
*   **피드 형식 오류**: 잘못된 XML 형식, 인코딩 문제
    *   `feedparser`의 예외 처리 활용
    *   로그 기록 후 다음 피드로 진행

### 5.2. Gemini API 관련
*   **API 호출 실패**: 네트워크 오류, 인증 실패
    *   재시도 로직 (지수 백오프 적용)
    *   사용자에게 명확한 에러 메시지 표시
*   **할당량 초과**: Rate Limit 도달
    *   대기 시간 후 재시도
    *   일일 할당량 모니터링 및 경고
*   **응답 형식 오류**: JSON 파싱 실패
    *   응답 검증 로직 추가
    *   기본값으로 대체하거나 재요청

### 5.3. GitHub API 관련
*   **인증 실패**: 잘못된 토큰 또는 권한 부족
    *   토큰 유효성 검사
    *   사용자에게 Secrets 재설정 안내
*   **커밋 실패**: 충돌, 네트워크 오류
    *   최신 상태로 Pull 후 재시도
    *   로컬 백업 생성 후 나중에 동기화

### 5.4. 데이터 파일 관련
*   **JSON 파일 손상/누락**: 파일이 없거나 형식 오류
    *   기본값으로 초기화
    *   백업 파일에서 복구 시도
*   **날짜별 데이터 없음**: 선택한 날짜에 데이터가 없는 경우
    *   친절한 안내 메시지 표시
    *   가장 최근 날짜 데이터 추천

---

## 6. 단계별 개발 가이드 (Cursor AI 프롬프트용)

### **1단계: 기본 환경 구축 및 UI 구조 잡기**
> "Streamlit을 사용하여 사이드바 메뉴(메인 뉴스룸, 관리자 대시보드)가 있는 앱의 기본 구조를 만들어줘. 데이터는 `data/` 폴더 안의 JSON 파일들을 읽어오는 방식으로 초기화해줘."

### **2단계: RSS 수집 및 Gemini API 연동**
> "RSS 피드 URL 리스트를 받아 내용을 파싱하고, 그 결과를 Google Gemini API(1.5 Flash)에 보내서 IT 뉴스 요약 브리핑을 만드는 함수를 작성해줘. 결과는 지정된 JSON 형식으로 리턴해야 해."

### **3단계: GitHub API를 이용한 데이터 영구 저장**
> "Streamlit 앱에서 생성된 JSON 데이터를 내 GitHub 리포지토리에 직접 커밋하고 푸시하는 기능을 추가해줘. PyGithub 라이브러리를 사용하고 API 토큰은 `st.secrets`에서 가져오도록 해줘."

### **4단계: 방문자 통계 기능**
> "사용자가 접속할 때마다 `stats.json`에 날짜별로 카운트를 올리는 기능을 만들고, 대시보드에서 이를 간단한 선 그래프로 보여줘."

### **5단계: 메인 뉴스룸 디자인 개선**
> "메인 화면의 뉴스 요약 결과가 잡지나 뉴스레터처럼 보이도록 CSS를 활용해서 스타일링해줘. 가독성을 위해 이모지와 섹션 구분을 명확히 해줘."

### **6단계: 에러 처리 및 로깅 추가**
> "RSS 피드 접근 실패, API 호출 실패, JSON 파일 오류 등 다양한 예외 상황을 처리하는 로직을 추가해줘. 사용자에게는 친절한 메시지를 보여주고, 개발자용으로는 상세 로그를 기록하도록 해줘."

---

## 7. 배포 및 운영 시나리오

### 7.1. 초기 배포
1.  **로컬 개발**: Cursor AI에서 코드를 작성하고 테스트.
2.  **GitHub 푸시**: 작성된 코드를 GitHub 리포지토리에 업로드.
3.  **Streamlit Cloud 연결**: 리포지토리 배포 설정.
4.  **환경 변수 입력**: Gemini API Key와 GitHub 토큰을 Secrets에 등록.
5.  **초기 데이터 생성**: `data/` 폴더에 빈 JSON 파일들 생성 (`feeds.json`, `news_data.json`, `stats.json`).

### 7.2. 일일 운영
*   **수동 운영**: 매일 아침 대시보드에 접속해 '수집 시작' → 'AI 브리핑 생성' 버튼을 눌러 뉴스룸 업데이트.
*   **자동화 (GitHub Actions)**: 
    *   `.github/workflows/daily-news.yml` 파일 생성
    *   매일 특정 시간(예: 오전 9시)에 자동으로 RSS 수집 및 AI 분석 실행
    *   결과를 GitHub 리포지토리에 자동 커밋
    *   실패 시 이메일 또는 Slack 알림 설정

### 7.3. GitHub Actions 자동화 예시
```yaml
name: Daily News Update
on:
  schedule:
    - cron: '0 0 * * *'  # 매일 UTC 자정 (한국시간 오전 9시)
  workflow_dispatch:  # 수동 실행도 가능

jobs:
  update-news:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run news collection
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/daily_update.py
```

### 7.4. 모니터링 및 유지보수
*   **데이터 백업**: 주기적으로 JSON 파일들을 별도 브랜치나 외부 저장소에 백업
*   **성능 모니터링**: API 호출 시간, 에러 발생 빈도 추적
*   **피드 관리**: 주기적으로 RSS 피드 유효성 검사 및 업데이트
*   **사용자 피드백**: Streamlit 앱 내 피드백 수집 기능 추가 고려