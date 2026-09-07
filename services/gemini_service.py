import os
from typing import List
from google import genai
from google.genai import types
from services.github_service import RepoActivity

def load_skill(filename: str) -> str:
    """Carrega dinamicamente o conteúdo na íntegra de uma skill do diretório /skills"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_path = os.path.join(base_dir, "skills", filename)
    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

class GeminiService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_daily_report(self, activities: List[RepoActivity], pm_name: str = "Eduardo Gois") -> str:
        if not activities:
            return "📌 **Resumo Diário GitHub**: Nenhuma alteração foi registrada nos repositórios da Mangue House nas últimas 24 horas."

        formatted_logs = []
        for act in activities:
            commits_str = "\n".join([f"  - [{c.sha}] {c.message} (autor: {c.author})" for c in act.commits]) or "  (Nenhum commit direto)"
            prs_str = "\n".join([f"  - PR #{p.number}: {p.title} [{p.state}{' / MERGED' if p.merged else ''}] (autor: {p.author})" for p in act.pull_requests]) or "  (Nenhum PR recente)"
            formatted_logs.append(f"Projeto / Repositório: {act.repo_name}\nCommits:\n{commits_str}\nPull Requests:\n{prs_str}")

        activity_text = "\n\n---\n\n".join(formatted_logs)

        # Carrega o conteúdo na íntegra das 4 skills do bot
        humanizer_skill = load_skill("humanizer.md")
        release_notes_skill = load_skill("release-notes.md")
        commit_work_skill = load_skill("commit-work.md")
        pre_mortem_skill = load_skill("pre-mortem.md")

        system_instruction = f"""
Você é o assistente de gestão de produto de {pm_name} na Mangue House. Seu objetivo é analisar as alterações do GitHub (commits e PRs) e gerar um relatório diário no formato de Release Notes Executivo de Produto.

Siga rigorosamente as diretrizes e regras das 4 skills completas abaixo:

=== SKILL 1: HUMANIZER (Linguagem Humana e Remoção de Clichês) ===
{humanizer_skill}

=== SKILL 2: RELEASE NOTES (Categorização e Tradução para Benefício do Usuário) ===
{release_notes_skill}

=== SKILL 3: COMMIT WORK (Taxonomia Conventional Commits) ===
{commit_work_skill}

=== SKILL 4: PRE-MORTEM (Análise Preditiva de Riscos e Elephants) ===
{pre_mortem_skill}

REGRAS FINAIS DE SAÍDA PARA O DISCORD:
- Escreva a resposta em Português do Brasil.
- Comece diretamente com: 📌 Resumo de Atividades & Release Notes - Mangue House
- Para cada repositório com atividade, crie um cabeçalho `### [Nome do Repositório]`
- Organize em: 🚀 **Novas Funcionalidades**, ⚡ **Melhorias**, 🐛 **Correções de Bugs**, ⚠️ **Atenção & Riscos (Pre-Mortem)**
- NUNCA inclua saudações iniciais ("Olá", "Aqui está o relatório") nem despedidas robóticas ("Espero que ajude", "Se tiver dúvidas").
- Aplique o Pre-Mortem em ⚠️ **Atenção & Riscos**: sinalize *Tigers* (riscos reais no código/PR) e *Elephants* (commits vagos ou suposições sem contexto no Git).
"""

        user_prompt = f"""
Aqui estão os logs brutos das alterações ocorridas nas últimas 24 horas nos repositórios:

{activity_text}

Gere o relatório formatado para o Discord aplicando na íntegra as 4 skills fornecidas acima.
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
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
