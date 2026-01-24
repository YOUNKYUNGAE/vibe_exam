"""
GitHub API를 사용한 데이터 영구 저장 모듈
"""
from github import Github
from github.GithubException import GithubException
import json
import logging
from pathlib import Path
import streamlit as st

logger = logging.getLogger(__name__)

class GitHubManager:
    """GitHub API를 사용하여 데이터를 저장하는 클래스"""
    
    def __init__(self):
        self.repo = None
        self._initialize_client()
    
    def _initialize_client(self):
        """GitHub API 클라이언트 초기화"""
        try:
            # Streamlit secrets에서 토큰 가져오기
            try:
                token = st.secrets.get("GITHUB_TOKEN", "")
                repo_name = st.secrets.get("GITHUB_REPO", "")
            except:
                # secrets가 없으면 환경 변수에서 시도
                import os
                token = os.getenv("GITHUB_TOKEN", "")
                repo_name = os.getenv("GITHUB_REPO", "")
            
            if not token:
                logger.warning("GITHUB_TOKEN이 설정되지 않았습니다.")
                self.client_initialized = False
                return
            
            if not repo_name:
                logger.warning("GITHUB_REPO가 설정되지 않았습니다.")
                self.client_initialized = False
                return
            
            g = Github(token)
            self.repo = g.get_repo(repo_name)
            self.client_initialized = True
            
        except Exception as e:
            logger.error(f"GitHub API 초기화 실패: {e}")
            self.client_initialized = False
    
    def save_json_file(self, filename: str, data: dict, commit_message: str = None):
        """
        JSON 파일을 GitHub 리포지토리에 저장합니다.
        
        Args:
            filename: 저장할 파일명 (예: "data/news_data.json")
            data: 저장할 데이터
            commit_message: 커밋 메시지
            
        Returns:
            저장 결과 딕셔너리
        """
        if not self.client_initialized:
            # GitHub가 초기화되지 않았으면 로컬에만 저장
            return self._save_local(filename, data)
        
        try:
            # JSON 문자열로 변환
            json_content = json.dumps(data, ensure_ascii=False, indent=2)
            
            # 파일 경로
            file_path = f"data/{filename}" if not filename.startswith("data/") else filename
            
            # 커밋 메시지
            if not commit_message:
                commit_message = f"Update {filename}"
            
            # 파일이 존재하는지 확인
            try:
                contents = self.repo.get_contents(file_path)
                # 파일이 존재하면 업데이트
                self.repo.update_file(
                    file_path,
                    commit_message,
                    json_content,
                    contents.sha
                )
            except GithubException as e:
                if e.status == 404:
                    # 파일이 없으면 생성
                    self.repo.create_file(
                        file_path,
                        commit_message,
                        json_content
                    )
                else:
                    raise
            
            return {
                'success': True,
                'message': f'{filename} 저장 완료'
            }
            
        except GithubException as e:
            logger.error(f"GitHub 저장 실패: {e}")
            # 실패 시 로컬에 저장
            local_result = self._save_local(filename, data)
            local_result['github_error'] = str(e)
            return local_result
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            local_result = self._save_local(filename, data)
            local_result['error'] = str(e)
            return local_result
    
    def _save_local(self, filename: str, data: dict):
        """로컬에 JSON 파일 저장 (백업용)"""
        try:
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            file_path = data_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return {
                'success': True,
                'message': f'{filename} 로컬 저장 완료',
                'local_only': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'로컬 저장 실패: {str(e)}'
            }
    
    def load_json_file(self, filename: str):
        """
        GitHub 리포지토리에서 JSON 파일을 로드합니다.
        
        Args:
            filename: 로드할 파일명
            
        Returns:
            로드된 데이터 또는 빈 딕셔너리
        """
        # 먼저 로컬에서 시도
        local_path = Path("data") / filename
        if local_path.exists():
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"로컬 파일 로드 실패: {e}")
        
        # GitHub에서 로드 시도
        if not self.client_initialized:
            return {}
        
        try:
            file_path = f"data/{filename}" if not filename.startswith("data/") else filename
            contents = self.repo.get_contents(file_path)
            return json.loads(contents.decoded_content.decode('utf-8'))
        except GithubException as e:
            if e.status == 404:
                logger.info(f"파일이 존재하지 않음: {filename}")
                return {}
            else:
                logger.error(f"GitHub 로드 실패: {e}")
                return {}
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            return {}
