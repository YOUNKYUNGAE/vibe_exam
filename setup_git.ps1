# PowerShell 스크립트 - GitHub 리포지토리 설정

Write-Host "🚀 GitHub 리포지토리 설정 시작..." -ForegroundColor Cyan

# Git 초기화 확인
if (-not (Test-Path .git)) {
    git init
    Write-Host "✅ Git 초기화 완료" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Git이 이미 초기화되어 있습니다" -ForegroundColor Yellow
}

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: AI 기반 IT 뉴스룸 앱"

# 리모트 확인 및 추가
$remoteExists = git remote | Select-String "origin"
if ($remoteExists) {
    Write-Host "ℹ️  리모트 'origin'이 이미 설정되어 있습니다" -ForegroundColor Yellow
    git remote set-url origin https://github.com/YOUNKYUNGAE/vibe_exam.git
} else {
    git remote add origin https://github.com/YOUNKYUNGAE/vibe_exam.git
    Write-Host "✅ 리모트 'origin' 추가 완료" -ForegroundColor Green
}

# 브랜치 이름 변경 및 푸시
git branch -M main
Write-Host "📤 GitHub에 푸시 중..." -ForegroundColor Cyan
git push -u origin main

Write-Host "✅ 완료! 이제 Streamlit Cloud에서 배포할 수 있습니다." -ForegroundColor Green
