import os
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import resend

from ai_client import generate_frontier, generate_basics, generate_job
from github_trending import fetch_github_trending, format_trending_markdown

load_dotenv()

BEIJING_TZ = timezone(timedelta(hours=8))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def build_email_html(frontier, basics, trending, job, date_str):
    return f"""
    <html>
    <body style="font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background-color: #f5f7fa;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="margin: 0; font-size: 26px;">📬 AI 每日学习速报</h1>
            <p style="margin: 8px 0 0; opacity: 0.9;">{date_str}</p>
        </div>

        <div style="background: white; padding: 25px; border-radius: 0 0 12px 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">

            <div style="margin-bottom: 30px; border-left: 4px solid #667eea; padding-left: 16px;">
                <h2 style="color: #333; margin-top: 0;">🔷 今日前沿</h2>
                {frontier.replace('🔷', '').strip()}
            </div>

            <div style="margin-bottom: 30px; border-left: 4px solid #38a169; padding-left: 16px;">
                <h2 style="color: #333; margin-top: 0;">🔷 今日基础</h2>
                {basics.replace('🔷', '').strip()}
            </div>

            <div style="margin-bottom: 30px; border-left: 4px solid #ecc94b; padding-left: 16px;">
                <h2 style="color: #333; margin-top: 0;">🟢 GitHub 热点速递</h2>
                {trending}
            </div>

            <div style="margin-bottom: 20px; border-left: 4px solid #ed8936; padding-left: 16px;">
                <h2 style="color: #333; margin-top: 0;">🟡 今日AI岗位</h2>
                {job.replace('🟡', '').strip()}
            </div>

            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 25px 0;">
            <p style="color: #a0aec0; font-size: 12px; text-align: center;">
                📮 由 AI 自动生成并推送 | 内容仅供参考学习<br>
                <a href="https://github.com/trending" style="color: #667eea;">GitHub Trending</a> ·
                技术前沿追踪
            </p>
        </div>
    </body>
    </html>
    """

def send_email(content_html):
    resend.api_key = os.getenv("RESEND_API_KEY")
    target_email = os.getenv("TARGET_EMAIL")

    if not target_email:
        logger.error("请在 .env 中设置 TARGET_EMAIL")
        return False

    params: resend.Emails.SendParams = {
        "from": "AI学习速报 <onboarding@resend.dev>",
        "to": [target_email],
        "subject": f"📬 AI每日学习速报 - {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d')}",
        "html": content_html,
    }

    try:
        email_response = resend.Emails.send(params)
        logger.info(f"✅ 邮件已发送! ID: {email_response.get('id', 'N/A')}")
        return True
    except Exception as e:
        logger.error(f"❌ 邮件发送失败: {e}")
        return False

def daily_job():
    today = datetime.now(BEIJING_TZ)
    date_str = today.strftime('%Y年%m月%d日')

    logger.info(f"========== 开始执行每日推送: {date_str} ==========")

    try:
        repos = fetch_github_trending(period="daily", limit=5)
        trending_md = format_trending_markdown(repos)
        logger.info(f"GitHub热点抓取: {len(repos)} 个项目")
    except Exception as e:
        logger.error(f"GitHub抓取失败: {e}")
        trending_md = "今日 GitHub 热点数据暂不可用，请稍后再试。"

    logger.info("开始生成AI内容...")
    frontier = generate_frontier()
    logger.info("  ✅ 前沿模块完成")
    basics = generate_basics()
    logger.info("  ✅ 基础模块完成")
    job = generate_job()
    logger.info("  ✅ 岗位模块完成")

    html = build_email_html(frontier, basics, trending_md, job, date_str)

    success = send_email(html)
    if success:
        logger.info("========== 每日推送完成 ✅ ==========")
    else:
        logger.error("========== 推送失败 ❌ ==========")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--now":
        logger.info("手动执行一次...")
        daily_job()
    elif len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        import schedule
        import time
        schedule.every().day.at("08:00").do(daily_job)
        logger.info("⏰ 定时任务已启动，每天 08:00 执行推送")
        while True:
            schedule.run_pending()
            time.sleep(30)
    else:
        print("用法:")
        print("  python main.py --now       # 立即执行一次")
        print("  python main.py --schedule  # 启动定时任务（每天08:00）")