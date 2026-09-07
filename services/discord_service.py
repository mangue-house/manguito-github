import requests
import time
from typing import List

class DiscordService:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_message(self, content: str) -> None:
        chunks = self._split_message(content, max_length=1900)

        for i, chunk in enumerate(chunks):
            payload = {
                "content": chunk,
                "username": "Mangue House GitHub Bot",
                "avatar_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
            }

            resp = requests.post(self.webhook_url, json=payload, headers={"Content-Type": "application/json"})
            if resp.status_code not in (200, 204):
                print(f"❌ Erro ao enviar para o Discord (parte {i+1}/{len(chunks)}): HTTP {resp.status_code} - {resp.text}")
                resp.raise_for_status()

            if len(chunks) > 1:
                time.sleep(0.5)

    def _split_message(self, text: str, max_length: int = 1900) -> List[str]:
        if len(text) <= max_length:
            return [text]

        lines = text.split("\n")
        chunks = []
        current_chunk = ""

        for line in lines:
            if len(current_chunk + "\n" + line) > max_length:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = line
            else:
                current_chunk += ("\n" if current_chunk else "") + line

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks
