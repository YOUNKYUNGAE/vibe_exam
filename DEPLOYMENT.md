# 🚀 Streamlit Cloud 배포 가이드

## 1단계: GitHub 리포지토리 준비

### 로컬에서 Git 초기화 및 푸시

```bash
# Git 초기화 (아직 안 했다면)
git init

# 모든 파일 추가 (단, .env는 제외됨 - .gitignore에 포함)
git add .

# 첫 커밋
git commit -m "Initial commit: AI 기반 IT 뉴스룸 앱"

# GitHub 리포지토리 연결 (이미 있다면)
git remote add origin https://github.com/YOUNKYUNGAE/vibe_exam.git

# 또는 새로 만들려면
# GitHub에서 새 리포지토리 생성 후:
# git remote add origin https://github.com/YOUNKYUNGAE/vibe_exam.git

# 푸시
git branch -M main
git push -u origin main
```

## 2단계: Streamlit Cloud 연결

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인

2. **앱 배포**
   - "New app" 버튼 클릭
   - GitHub 리포지토리 선택: `YOUNKYUNGAE/vibe_exam`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: 원하는 URL 입력 (예: `my-it-newsroom`)

3. **Secrets 설정** (중요!)
   - 배포 페이지에서 "Secrets" 탭 클릭
   - 또는 앱 설정에서 "Secrets" 메뉴 선택
   - 다음 내용을 입력:

```toml
GEMINI_API_KEY = "AIzaSyC_WKlKD7benooSdNRE4ncZGUw-q0ea6jg"
GITHUB_TOKEN = "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"
GITHUB_REPO = "YOUNKYUNGAE/vibe_exam"
```

## 3단계: 배포 확인

1. Streamlit Cloud가 자동으로 앱을 빌드하고 배포합니다
2. 배포 완료 후 제공되는 URL로 접속 (예: `https://my-it-newsroom.streamlit.app`)
3. 앱이 정상적으로 작동하는지 확인

## 4단계: 자동 업데이트

- GitHub에 코드를 푸시하면 Streamlit Cloud가 자동으로 재배포합니다
- Secrets는 Streamlit Cloud 대시보드에서만 수정 가능합니다

## ⚠️ 보안 주의사항

- ✅ `.env` 파일은 `.gitignore`에 포함되어 있어 GitHub에 업로드되지 않습니다
- ✅ API 키와 토큰은 Streamlit Cloud의 Secrets에만 저장합니다
- ❌ 절대 코드에 API 키를 하드코딩하지 마세요
- ❌ GitHub에 `.env` 파일을 커밋하지 마세요

## 🔧 문제 해결

### 배포 실패 시
1. Streamlit Cloud 로그 확인
2. `requirements.txt`에 모든 의존성이 포함되어 있는지 확인
3. Python 버전 호환성 확인 (3.8+)

### Secrets 오류 시
1. Secrets 형식이 올바른지 확인 (TOML 형식)
2. 따옴표가 올바르게 닫혀있는지 확인
3. 앱 재배포
