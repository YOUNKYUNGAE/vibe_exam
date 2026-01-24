# 🌐 Streamlit Cloud 배포 단계별 가이드

## 현재 상황
- 로컬에서 HTTP로 실행 중이라 브라우저 보안 문제로 접속 불가
- Streamlit Cloud에 배포하면 HTTPS로 안전하게 접속 가능

## 📋 배포 단계

### 1단계: Git 변경사항 커밋 및 푸시

터미널에서 다음 명령어를 실행하세요:

```powershell
cd c:\Users\huare\Desktop\cursor_test

# 변경사항 확인
git status

# 모든 변경사항 추가 (secrets.toml은 .gitignore에 있어서 자동 제외됨)
git add .

# 커밋
git commit -m "Update configuration for Streamlit Cloud deployment"

# GitHub에 푸시
git push origin main
```

**참고**: GitHub 인증이 필요할 수 있습니다. Personal Access Token을 사용하거나 GitHub Desktop을 사용하세요.

---

### 2단계: Streamlit Cloud에 배포

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인 (처음이면 회원가입)

2. **새 앱 생성**
   - "New app" 버튼 클릭
   - 다음 정보 입력:
     - **Repository**: `YOUNKYUNGAE/vibe_exam` 선택
     - **Branch**: `main`
     - **Main file path**: `app.py`
     - **App URL**: 원하는 이름 입력 (예: `my-it-newsroom`)

3. **Secrets 설정** (중요!)
   - 배포 설정 페이지에서 "Advanced settings" 또는 "Secrets" 탭 클릭
   - 다음 내용을 입력:

```toml
GEMINI_API_KEY = "AIzaSyC_WKlKD7benooSdNRE4ncZGUw-q0ea6jg"
GITHUB_REPO = "YOUNKYUNGAE/vibe_exam"
```

   - GitHub Token이 필요하면 추가:
```toml
GITHUB_TOKEN = "your-github-token-here"
```

4. **배포 시작**
   - "Deploy!" 버튼 클릭
   - Streamlit Cloud가 자동으로 빌드하고 배포합니다 (약 1-2분 소요)

---

### 3단계: 배포 확인

1. 배포 완료 후 제공되는 URL로 접속
   - 예: `https://my-it-newsroom.streamlit.app`
   - **HTTPS로 안전하게 접속 가능합니다!**

2. 앱이 정상 작동하는지 확인
   - 메인 뉴스룸 페이지 확인
   - 관리자 대시보드 확인

---

## ✅ 배포 완료 후

- **자동 업데이트**: GitHub에 코드를 푸시하면 자동으로 재배포됩니다
- **Secrets 수정**: Streamlit Cloud 대시보드에서만 수정 가능
- **로그 확인**: Streamlit Cloud 대시보드에서 앱 로그 확인 가능

---

## 🔧 문제 해결

### 배포 실패 시
1. Streamlit Cloud 대시보드에서 로그 확인
2. `requirements.txt`에 모든 의존성이 포함되어 있는지 확인
3. Python 버전 호환성 확인 (3.8+)

### Secrets 오류 시
1. Secrets 형식이 올바른지 확인 (TOML 형식)
2. 따옴표가 올바르게 닫혀있는지 확인
3. 앱 재배포

### Git 푸시 문제 시
- GitHub Personal Access Token 사용
- 또는 GitHub Desktop 사용

---

## 🎉 완료!

배포가 완료되면 HTTPS URL로 언제든지 접속할 수 있습니다!
