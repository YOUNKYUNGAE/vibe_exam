# 🚀 빠른 시작 가이드

## 로컬에서 실행하기

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. Secrets 설정
`.streamlit/secrets.toml` 파일을 생성하고 다음 내용을 입력:
```toml
GEMINI_API_KEY = "your-api-key"
GITHUB_TOKEN = "your-token"  # 선택사항
GITHUB_REPO = "username/repo"  # 선택사항
```

### 3. 앱 실행
```bash
streamlit run app.py
```

## Streamlit Cloud에 배포하기

### 1. GitHub에 푸시
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUNKYUNGAE/vibe_exam.git
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloud 연결
1. https://streamlit.io/cloud 접속
2. "New app" 클릭
3. Repository: `YOUNKYUNGAE/vibe_exam` 선택
4. Main file: `app.py`
5. Secrets에 API 키 입력

### 3. 배포 완료!
자동으로 배포되고 URL이 제공됩니다.
