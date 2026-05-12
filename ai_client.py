import requests
import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

def ask_deepseek(prompt, max_tokens=2000):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=data, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"❌ API请求失败，状态码：{resp.status_code}，信息：{resp.text}"
    except Exception as e:
        return f"❌ 网络或其它错误：{e}"

def generate_frontier():
    prompt = "请讲解一个AI领域最前沿的技术或趋势（2026年最新），用🔷标记标题，300字以内，包含核心突破、为何重要两个部分。"
    return ask_deepseek(prompt, max_tokens=800)

def generate_basics():
    prompt = "请讲解一个AI最基础的概念：损失函数。用🔷标记标题，300字以内，包含核心原理、为何重要两个部分。"
    return ask_deepseek(prompt, max_tokens=800)

def generate_job():
    prompt = "请介绍一个AI职业：提示词工程师。用🟡标记标题，包含岗位画像、技能需求、薪资前景、给新人的建议四部分，300字以内。"
    return ask_deepseek(prompt, max_tokens=800)