#!/bin/bash
# GitHub 리포지토리 초기화 및 푸시 스크립트

echo "🚀 GitHub 리포지토리 설정 시작..."

# Git 초기화 (이미 되어있다면 스킵)
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git 초기화 완료"
else
    echo "ℹ️  Git이 이미 초기화되어 있습니다"
fi

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: AI 기반 IT 뉴스룸 앱"

# 리모트 확인 및 추가
if git remote | grep -q "origin"; then
    echo "ℹ️  리모트 'origin'이 이미 설정되어 있습니다"
    git remote set-url origin https://github.com/YOUNKYUNGAE/vibe_exam.git
else
    git remote add origin https://github.com/YOUNKYUNGAE/vibe_exam.git
    echo "✅ 리모트 'origin' 추가 완료"
fi

# 브랜치 이름 변경 및 푸시
git branch -M main
echo "📤 GitHub에 푸시 중..."
git push -u origin main

echo "✅ 완료! 이제 Streamlit Cloud에서 배포할 수 있습니다."
