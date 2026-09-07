# Discordito: Automação de Relatórios Diários do GitHub (Python)

Automação em Python desenvolvida para a **Mangue House** que coleta diariamente as alterações em todos os repositórios da organização no GitHub, sintetiza as entregas através da API do Gemini (`gemini-2.5-flash` + skill `humanizer`) e envia um resumo executivo de produto às 22:00 BRT no Discord para o PM Eduardo Gois.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.11+
- **IA**: Google Gemini API (`google-genai` SDK)
- **Integração Git**: GitHub REST API (`requests`)
- **Notificação**: Discord Webhooks
- **Execução / Agendamento**: GitHub Actions (`.github/workflows/daily-report.yml`) às 22h BRT

---

## 🚀 Como Executar Localmente

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` baseado no `.env.example`:
```env
GITHUB_TOKEN=ghp_seu_token_aqui
GITHUB_ORG=MangueHouse
GEMINI_API_KEY=AIzaSy_sua_chave_gemini
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/sua_url_webhook
```

### 3. Rodar o Relatório
```bash
python main.py
```

### 4. Rodar os Testes
```bash
pytest
```

---

## ⚙️ Configuração no GitHub Actions

No repositório do GitHub, configure as seguintes variáveis em **Settings > Secrets and variables > Actions**:

### Secrets
- `GEMINI_API_KEY`: Chave da API do Google Gemini.
- `DISCORD_WEBHOOK_URL`: URL do Webhook do canal do Discord.
- `GH_PAT_TOKEN` (opcional): Personal Access Token do GitHub se o repositório for privado/org.

### Variables (Opcional)
- `GITHUB_ORG`: Nome da organização (Default: `MangueHouse`).
