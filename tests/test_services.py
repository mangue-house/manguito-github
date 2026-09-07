import pytest
from services.discord_service import DiscordService
from services.github_service import RepoActivity, CommitInfo, PRInfo

def test_discord_message_splitting():
    svc = DiscordService("https://httpbin.org/post")
    
    # Text shorter than 1900 chars
    short_text = "Hello World\nLine 2"
    chunks = svc._split_message(short_text, max_length=100)
    assert len(chunks) == 1
    assert chunks[0] == short_text

    # Text longer than max length
    long_text = "\n".join([f"Line {i} - " + "x" * 20 for i in range(20)])
    chunks_long = svc._split_message(long_text, max_length=150)
    assert len(chunks_long) > 1
    for c in chunks_long:
        assert len(c) <= 150

def test_repo_activity_model():
    act = RepoActivity(
        repo_name="Mangue-Point",
        commits=[
            CommitInfo(sha="abc1234", message="feat: add pages API", author="Raul", date="2026-09-07", url="https://github.com/test/1")
        ],
        pull_requests=[
            PRInfo(number=8, title="MANGUEHOU-8 automation", author="Raul", state="closed", merged=True, url="https://github.com/test/pr/8")
        ]
    )
    assert act.repo_name == "Mangue-Point"
    assert len(act.commits) == 1
    assert act.pull_requests[0].merged is True
