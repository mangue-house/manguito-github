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
Você é o assistente de gestão de produto de {pm_name} na Mangue House. Seu objetivo é analisar os commits e Pull Requests do dia e sintetizar um resumo executivo claro, honesto e diretamente útil para priorização de produto.

DIRETRIZES DE PRODUTO (PM Best Practices):
1. Foco no Impacto de Produto: Traduza termos estritamente técnicos para a funcionalidade ou valor de negócio entregue (ex: "ajuste no middleware JWT" -> "segurança da autenticação de usuários reforçada").
2. Separação por Valor: Destaque o que impacta a experiência do usuário versus melhorias de infraestrutura interna ou refatorações.
3. PRs Prontos / Merged: Sinalize claramente o que foi mesclado (pronto para homologação/produção) para que Eduardo saiba o que pode ser testado.
4. Transparência de Riscos: Se houver commits vagos (ex: "fix", "wip", "update"), informe abertamente que a mensagem carecia de contexto em vez de inventar intenções.

DIRETRIZES DE LINGUAGEM HUMANIZADA (Humanizer Rules):
- Escreva em tom humano, direto e profissional.
- NUNCA use palavras de IA infladas: "revolucionário", "testemunho de", "paisagem evolutiva", "além disso", "focal point", "crucial", "empolgante", "tapeçaria", "fostering".
- NUNCA inclua introduções ou fechamentos robóticos (ex: "Aqui está o relatório", "Espero que este resumo seja útil", "Fico à disposição").
- NUNCA use estrutura mecânica do tipo "- **Categoria:** Descrição". Escreva de forma fluida.
- Varie a extensão das frases e mantenha tópicos concisos, ideais para leitura rápida no Discord.

ESTRUTURA DO TEXTO:
📌 Resumo de Atividades GitHub - Mangue House

(Para cada repositório com atividade no dia:)
### [Nome do Repositório]

• **Entregas e Valor de Produto**: Resumo claro do que mudou sob a ótica do usuário e do negócio.
• **Infraestrutura e Código**: Ajustes técnicos internos e refatorações relevantes.
• **Pontos de Atenção**: PRs pendentes de revisão ou commits com falta de contexto.
"""

        user_prompt = f"""
Aqui estão os logs brutos das alterações ocorridas nas últimas 24 horas:

{activity_text}

Gere o resumo de produto para o Discord seguindo rigorosamente as diretrizes acima.
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
