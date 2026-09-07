import sys
from config import get_config
from services.github_service import GitHubService
from services.gemini_service import GeminiService
from services.discord_service import DiscordService

def run_report_workflow():
    print("🚀 Iniciando rotina de geração do relatório diário do GitHub (Python)...")
    config = get_config()

    github_svc = GitHubService(config.github_token, config.github_org)
    gemini_svc = GeminiService(config.gemini_api_key)
    discord_svc = DiscordService(config.discord_webhook_url)

    print(f"📥 Coletando atividades do GitHub da organização '{config.github_org}'...")
    activities = github_svc.get_daily_activity(hours_ago=24)
    print(f"📊 Repositórios com atividade no dia: {len(activities)}")

    if not activities:
        print("ℹ️ Nenhuma atividade nas últimas 24h. Enviando mensagem padrão...")
        discord_svc.send_message("@everyone **Relatório Diário Github Mangue House**\n\nNenhuma alteração foi registrada nos repositórios da Mangue House nas últimas 24 horas.")
        print("✅ Notificação enviada.")
        return

    print("🧠 Sintetizando relatório executivo de produto via Gemini 2.5 Flash + Humanizer...")
    report_md = gemini_svc.generate_daily_report(activities, pm_name="Eduardo Gois")

    print("📤 Enviando relatório para o canal do Discord...")
    discord_svc.send_message(report_md)

    print("✅ Relatório enviado com sucesso!")

if __name__ == "__main__":
    try:
        run_report_workflow()
    except Exception as e:
        print(f"❌ Erro fatal na execução: {e}")
        sys.exit(1)
