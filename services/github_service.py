import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from pydantic import BaseModel

class CommitInfo(BaseModel):
    sha: str
    message: str
    author: str
    date: str
    url: str

class PRInfo(BaseModel):
    number: int
    title: str
    author: str
    state: str
    merged: bool
    url: str

class RepoActivity(BaseModel):
    repo_name: str
    commits: List[CommitInfo]
    pull_requests: List[PRInfo]

class GitHubService:
    def __init__(self, token: str, org: str):
        self.token = token
        self.org = org
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MangueHouse-Discordito-Bot"
        }
        self.base_url = "https://api.github.com"

    def get_daily_activity(self, hours_ago: int = 24) -> List[RepoActivity]:
        since_dt = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
        since_iso = since_dt.isoformat()
        activities: List[RepoActivity] = []

        # 1. Listar repositórios da organização
        org_url = f"{self.base_url}/orgs/{self.org}/repos?type=all&sort=updated&per_page=50"
        resp = requests.get(org_url, headers=self.headers)
        
        if resp.status_code != 200:
            # Fallback para repositórios do usuário autenticado
            user_url = f"{self.base_url}/user/repos?sort=updated&per_page=50"
            resp = requests.get(user_url, headers=self.headers)
            if resp.status_code != 200:
                print(f"❌ Erro ao buscar repositórios do GitHub: HTTP {resp.status_code}")
                return []

        repos = resp.json()

        for repo in repos:
            repo_name = repo.get("name")
            owner = repo.get("owner", {}).get("login")

            # 2. Coletar commits
            commits: List[CommitInfo] = []
            commits_url = f"{self.base_url}/repos/{owner}/{repo_name}/commits?since={since_iso}&per_page=100"
            c_resp = requests.get(commits_url, headers=self.headers)
            if c_resp.status_code == 200:
                for c in c_resp.json():
                    commit_obj = c.get("commit", {})
                    author_obj = commit_obj.get("author", {})
                    commits.append(CommitInfo(
                        sha=c.get("sha", "")[:7],
                        message=commit_obj.get("message", "").split("\n")[0],
                        author=author_obj.get("name") or c.get("author", {}).get("login", "Dev"),
                        date=author_obj.get("date", since_iso),
                        url=c.get("html_url", "")
                    ))

            # 3. Coletar Pull Requests
            prs: List[PRInfo] = []
            prs_url = f"{self.base_url}/repos/{owner}/{repo_name}/pulls?state=all&sort=updated&direction=desc&per_page=30"
            p_resp = requests.get(prs_url, headers=self.headers)
            if p_resp.status_code == 200:
                for pr in p_resp.json():
                    updated_at_str = pr.get("updated_at")
                    if updated_at_str:
                        updated_at = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))
                        if updated_at >= since_dt:
                            prs.append(PRInfo(
                                number=pr.get("number"),
                                title=pr.get("title", ""),
                                author=pr.get("user", {}).get("login", "Dev"),
                                state=pr.get("state", "open"),
                                merged=bool(pr.get("merged_at")),
                                url=pr.get("html_url", "")
                            ))

            if commits or prs:
                activities.append(RepoActivity(
                    repo_name=repo_name,
                    commits=commits,
                    pull_requests=prs
                ))

        return activities
