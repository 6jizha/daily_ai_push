导入 os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 创建 DeepSeek 客户端，使用正确的门牌号
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
base_url=“https://api.deepseek.com”
)

def generate_section(prompt, max_tokens=2000):
    “调用 DeepSeek 生成内容”
    尝试:
        response = client.chat.completions.create(
            model="deepseek-chat",   # 稳定可靠的模型
            messages=[
                {
                    "role": "system",
                    "内容": “您是AI技术领域的资深导师，擅长用通俗易懂的语言讲解复杂概念。请用Markdown格式回复，包含标题、要点和总结。”
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ 生成失败: {e}"

def generate_frontier():
    """生成今日前沿内容"""
prompt ="请讲解一个AI领域最前沿的技术或趋势（2026年最新），
用🔷标记标题，300字以内，包含核心突破、为何重要两个部分。"""
    返回 生成段落(提示，最大标记数=800)

def generate_basics():
    """生成今日基础内容"""
提示 = """请讲解一个AI最基础的概念或知识点，
用🔷标记标题，300字以内，包含核心原理、为何重要两个部分。
今天要讲的概念请从以下列表中随机选一个你还没讲过的：
- 损失函数 (Loss Function)
- 反向传播 (Backpropagation)
- 激活函数 (Activation Function)
- 过拟合与正则化 (Overfitting & Regularization)
- 卷积神经网络 CNN
- 循环神经网络 RNN
- 词嵌入 (Word Embedding)
- 强化学习 (Reinforcement Learning)
- 生成对抗网络 GAN
- 迁移学习 (Transfer Learning)"""
    return generate_section(prompt, max_tokens=800)

def generate_job():
    """生成今日AI岗位内容"""
提示 = """请介绍一个与AI相关的职业（从技术研发、应用落地、治理合规中随机选一个），
用🟡标记标题，包含岗位画像、技能需求、薪资前景、给新人的建议四部分，300字以内。"""
    return generate_section(prompt, max_tokens=800)
