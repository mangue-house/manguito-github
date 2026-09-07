from typing import List
from google import genai
from google.genai import types
from services.github_service import RepoActivity

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

        system_instruction = f"""
Você é o assistente de gestão de produto de {pm_name} na Mangue House. Seu objetivo é analisar as alterações do GitHub (commits e PRs) e gerar um relatório diário no formato de Release Notes Executivo de Produto.

DIRETRIZES DE CATEGORIZAÇÃO (Skill Release Notes):
1. Transforme termos técnicos em Benefício ao Usuário/Negócio:
   - Exemplo Técnico: "Implemented Redis caching layer" -> "Painel de controle com carregamento 3x mais rápido".
2. Categorize as entregas de cada repositório em:
   - 🚀 **Novas Funcionalidades**: Recursos totalmente inéditos adicionados.
   - ⚡ **Melhorias**: Aprimoramentos de desempenho, UI, estabilidade ou refatorações de código.
   - 🐛 **Correções de Bugs**: Erros ou falhas resolvidos.
   - ⚠️ **Atenção & Breaking Changes**: PRs pendentes de revisão, mudanças críticas de API ou commits sem contexto.

DIRETRIZES DE LINGUAGEM HUMANIZADA (Humanizer Rules):
- Escreva em tom humano, direto e profissional.
- NUNCA use palavras de IA infladas ("revolucionário", "testemunho de", "paisagem evolutiva", "além disso", "focal point", "crucial", "empolgante", "tapeçaria").
- NUNCA inclua introduções ou fechamentos robóticos (ex: "Aqui estão as release notes", "Espero que ajude").
- Se um commit for vago (ex: "fix", "wip"), explicite abertamente em ⚠️ Atenção que a mensagem carecia de contexto.

ESTRUTURA DO TEXTO:
📌 Resumo de Atividades & Release Notes - Mangue House

(Para cada repositório com atividade no dia:)
### [Nome do Repositório]

🚀 **Novas Funcionalidades** (se houver)
• ...

⚡ **Melhorias** (se houver)
• ...

🐛 **Correções de Bugs** (se houver)
• ...

⚠️ **Atenção & Ações Pendentes** (se houver)
• ...
"""

        user_prompt = f"""
Aqui estão os logs brutos das alterações ocorridas nas últimas 24 horas:

{activity_text}

Gere o relatório formatado para o Discord seguindo rigorosamente a estrutura de Release Notes acima.
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
