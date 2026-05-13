import requests
import os
import resend
from datetime import datetime, timezone, timedelta

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
RESEND_KEY = os.environ.get("RESEND_API_KEY")
TARGET = os.environ.get("TARGET_EMAIL")
BEIJING_TZ = timezone(timedelta(hours=8))

def ask_ai(prompt, max_tokens=800):
    if not DEEPSEEK_KEY:
        return "API key missing"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=data, timeout=60)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"API error: {resp.status_code} {resp.text[:200]}"
    except Exception as e:
        return f"Network error: {e}"

def send_email(html_body):
    if not RESEND_KEY or not TARGET:
        print("Email config missing")
        return
    resend.api_key = RESEND_KEY
    try:
        resend.Emails.send({
            "from": "AI学习速报 <onboarding@resend.dev>",
            "to": [TARGET],
            "subject": f"AI每日学习速报 - {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d')}",
            "html": html_body
        })
        print("Email sent!")
    except Exception as e:
        print(f"Email failed: {e}")

today = datetime.now(BEIJING_TZ)
date_str = today.strftime("%Y年%m月%d日 %A")
print(f"开始 {date_str} 推送...")

# 恢复中文提示词
frontier = ask_ai("请讲解一个AI领域最前沿的技术或趋势（2026年），用'今日前沿'作标题，300字以内。")
basics = ask_ai("请讲解一个AI最基础的概念：损失函数。用'今日基础'作标题，300字以内。")
job = ask_ai("请介绍一个AI职业：提示词工程师。用'今日AI岗位'作标题，包含岗位画像、技能、薪资、建议，300字以内。")

html = f"""
<html>
<body style="font-family: sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background: #f5f7fa;">
<div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
<h1>📬 AI 每日学习速报</h1><p style="margin: 8px 0 0;">{date_str}</p>
</div>
<div style="background: white; padding: 25px; border-radius: 0 0 12px 12px;">
<h2>🔷 今日前沿</h2><p>{frontier}</p>
<h2>🔷 今日基础</h2><p>{basics}</p>
<h2>🟡 今日AI岗位</h2><p>{job}</p>
<hr><p style="color: #a0aec0; font-size: 12px; text-align: center;">📮 由 AI 自动生成并推送 | 内容仅供参考学习</p>
</div>
</body>
</html>
"""

send_email(html)
print("流程结束")
