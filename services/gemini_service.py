from typing import List
from google import genai
from google.genai import types
from services.github_service import RepoActivity

class GeminiService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_daily_report(self, activities: List[RepoActivity], pm_name: str = "Eduardo Gois") -> str:
        if not activities:
            return "Nenhuma alteração registrada nos repositórios nas últimas 24 horas."

        formatted_logs = []
        for act in activities:
            commits_str = "\n".join([f"  - [{c.sha}] {c.message} (autor: {c.author})" for c in act.commits]) or "  (Nenhum commit direto)"
            prs_str = "\n".join([f"  - PR #{p.number}: {p.title} [{p.state}{' / MERGED' if p.merged else ''}] (autor: {p.author})" for p in act.pull_requests]) or "  (Nenhum PR recente)"
            formatted_logs.append(f"Projeto / Repositório: {act.repo_name}\nCommits:\n{commits_str}\nPull Requests:\n{prs_str}")

        activity_text = "\n\n---\n\n".join(formatted_logs)

        system_instruction = f"""
Você é um assistente sênior de produto encarregado de enviar o resumo diário de atividades técnicas do GitHub para o PM {pm_name}.

DIRETRIZES RÍGIDAS DE LINGUAGEM (Skill Humanizer):
1. Escreva em português claro, direto e natural.
2. NUNCA use clichês de IA (ex: "revolucionário", "testemunho de", "paisagem evolutiva", "além disso", "focal point", "crucial", "empolgante").
3. NUNCA use saudações robóticas ou encerramentos genéricos ("Espero que este relatório ajude!", "O futuro é promissor").
4. Mantenha frases curtas, objetivas e fáceis de ler no celular.
5. Foco em PRODUTO: Explique O QUE mudou e POR QUE a mudança é relevante para a gestão de produto.
6. Se um commit tiver mensagem muito curta ou sem contexto (ex: "fix", "wip"), explicite de forma direta que a mensagem original carecia de contexto em vez de inventar especulações.

ESTRUTURA DO RELATÓRIO:
- Cabeçalho: 📌 Resumo Diário de Entregas - GitHub
- Seções por Projeto/Repositório
- Lista dos principais avanços e impactos de produto
- Alertas de atenção (commits vagos ou PRs pendentes, se houver)
"""

        user_prompt = f"""
Aqui estão os logs de atividades técnicas das últimas 24 horas:

{activity_text}

Por favor, crie o resumo executivo de produto formatado em Markdown para o Discord.
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                )
            )
            return response.text.strip() if response.text else "Não foi possível gerar o resumo automático."
        except Exception as e:
            print(f"❌ Erro ao chamar a API do Gemini: {e}")
            raise e
