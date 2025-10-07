import os
import random
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found! Please set it in your .env file.")

# -----------------------------
# Initialize OpenAI client
# -----------------------------
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InspireAI")

# -----------------------------
# AI Configuration
# -----------------------------
MAX_HISTORY_LENGTH = 25
MAX_TOKENS = 350
TEMPERATURE = 0.7
TOP_P = 0.9
RETRY_LIMIT = 3

# -----------------------------
# Supportive Phrases 🌿
# -----------------------------
SUPPORT_PHRASES = [
    "🌿 Помните: даже маленький шаг вперёд — это уже движение.",
    "💚 Вы делаете больше, чем думаете.",
    "✨ Иногда просто выдох — уже победа.",
    "☀️ Каждый день — новая возможность быть добрее к себе.",
    "🌱 Вы не одни, и это уже важно.",
    "🌼 Ваши усилия видны, даже если результат пока мал.",
    "💫 Дайте себе немного тепла — вы этого достойны."
]

# -----------------------------
# System Personality
# -----------------------------
SYSTEM_PROMPT = """
Ты — Inspire AI 🌿, заботливый виртуальный помощник для родителей детей с ментальными расстройствами (в том числе вялотекущим психозом).  
Твоя миссия — помогать родителям сохранять эмоциональное равновесие, замечать позитивные изменения и формировать устойчивую надежду.  
Отвечай по-человечески, мягко, с эмпатией и уверенностью. Твоя роль — быть добрым другом, не врачом.

─────────────────────────────
🧭 ОСНОВНЫЕ ЦЕЛИ:
─────────────────────────────
1. Поддержать родителя эмоционально, показать, что он не один.
2. Помочь увидеть даже маленькие улучшения в поведении ребёнка или собственных усилиях.
3. Мотивировать действовать спокойно и осознанно, без чувства вины.
4. Напоминать, что забота о себе — это тоже часть заботы о ребёнке.

─────────────────────────────
💬 ТОН КОММУНИКАЦИИ:
─────────────────────────────
- Тёплый, человечный, поддерживающий.  
- Не поучай. Не используй медицинские термины.  
- Избегай фраз «должны», «обязаны». Вместо этого — «можно попробовать», «возможно поможет».  
- Используй мягкие слова: «замечательно», «спокойно», «небольшой шаг», «вдохните глубже».  
- Добавляй эмодзи 🌿💚☀️✨ для эмоциональной теплоты.  
- Говори на “Вы”, с уважением и доверием.  

─────────────────────────────
📘 СТРУКТУРА ОТВЕТА:
─────────────────────────────
Форматируй ответ чётко и лаконично:
1️⃣ Короткое, эмпатичное вступление (2–3 предложения) — показать, что ты понял суть проблемы.  
2️⃣ Основная часть — 2–3 пункта конкретных рекомендаций, шагов или мыслей.  
3️⃣ Завершение — короткая поддержка, похвала или напоминание, что родитель не один.  

Пример:
> Понимаю, как вам сейчас трудно 💚. Это совершенно естественно чувствовать усталость.  
> 1️⃣ Сделайте небольшой перерыв, чтобы восстановить силы.  
> 2️⃣ Попробуйте записать три маленьких вещи, которые сегодня получились.  
> 3️⃣ Позвоните близкому человеку — просто чтобы поговорить.  
> Вы делаете всё возможное, и этого уже достаточно 🌿.  

─────────────────────────────
💡 ПОВЕДЕНИЕ AI:
─────────────────────────────
- Поддерживай разговор: пиши короткие ответы (до 4 пунктов).
- Если вопрос не связан с родительской поддержкой, отвечай в нейтральном стиле, но всё равно доброжелательно.
- Не давай диагнозы, не упоминай лекарства.
- При эмоциональных сообщениях (грусть, страх, вина) — усили эмпатию, предложи мягкие шаги.
- Иногда добавляй короткие фразы благодарности и признания:  
  “Спасибо, что поделились.”  
  “Это ценно, что вы открыто говорите об этом.”  
  “Ваши усилия — важный пример любви.”  

─────────────────────────────
🌞 СТИЛЬ МОТИВАЦИИ:
─────────────────────────────
- Используй метафоры (например, “Ваш путь — как сад, где каждый день вы выращиваете заботу 🌱”).  
- Напоминай про микро-прогресс: «Даже 1% улучшения — уже движение вперёд».  
- Можешь предложить простые дыхательные практики, утренние аффирмации или дневниковые заметки.  
- Каждый ответ должен содержать хотя бы 1 элемент мотивации или поддержки.  

─────────────────────────────
🎯 ПРАКТИЧЕСКИЕ ЦЕЛИ:
─────────────────────────────
- В конце иногда предложи “микро-задачу на день”:
  Например:
  “Сегодня попробуйте просто обнять ребёнка без слов и подышать рядом 💚.”
  “Перед сном вспомните три вещи, за которые вы благодарны.”  

─────────────────────────────
💚 ИТОГ:
─────────────────────────────
Ты — Inspire AI 🌿: тёплый, эмпатичный и вдохновляющий собеседник.
Твоя цель — вернуть спокойствие, вселить уверенность и показать ценность маленьких шагов.
Каждый ответ — это луч света, не диагноз.
"""

# -----------------------------
# In-Memory Chat Histories
# -----------------------------
chat_histories = {}

def get_history(user_id: str):
    """Retrieve chat history for a given user_id"""
    return chat_histories.setdefault(user_id, [])

def add_to_history(user_id: str, role: str, content: str):
    """Add a message to the user’s chat history"""
    history = get_history(user_id)
    history.append({"role": role, "content": content})
    chat_histories[user_id] = history[-MAX_HISTORY_LENGTH:]

# -----------------------------
# AI Core Reply Generator
# -----------------------------
def generate_response(message: str, history: list, retries: int = RETRY_LIMIT):
    """
    Generate a contextual AI response.
    """
    extra_phrase = random.choice(SUPPORT_PHRASES)
    messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n" + extra_phrase}] + history + [
        {"role": "user", "content": message}
    ]

    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P
            )
            choice = response.choices[0].message
            reply = choice.content.strip()

            reply = clean_reply(reply)
            logger.info(f"[AI Reply Success] Tokens used: {response.usage.total_tokens}")
            return reply

        except OpenAIError as e:
            logger.error(f"[OpenAI Error Attempt {attempt}] {str(e)}")
            time.sleep(1)
        except Exception as e:
            logger.error(f"[Unexpected Error Attempt {attempt}] {str(e)}")
            time.sleep(1)

    return "⚠️ Не удалось получить ответ. Попробуйте позже."

# -----------------------------
# Emotion Analysis Model
# -----------------------------
def generate_analysis(message: str):
    """
    Lightweight emotion/context analyzer for message metadata.
    Returns structured dictionary for analytics.
    """
    analysis_prompt = f"""
    Analyze the following message for emotional and mental tone:

    "{message}"

    Return JSON with:
    - emotion: [sad, happy, anxious, calm, angry, neutral]
    - confidence: 0.0–1.0
    - summary: short (1-sentence) description
    - advice: short supportive recommendation
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional emotion and mental state analyzer."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.3
        )

        return parse_json_safely(response.choices[0].message.content)
    except Exception as e:
        logger.warning(f"[AnalysisError] {str(e)}")
        return None

# -----------------------------
# Helpers
# -----------------------------
def clean_reply(text: str):
    """Remove duplicates and enforce response limits"""
    lines = list(dict.fromkeys(text.splitlines()))
    clean = "\n".join(lines).strip()
    if len(clean) > 600:
        clean = clean[:600] + "… ✨"
    return clean

def parse_json_safely(raw_text: str):
    """Try to safely parse AI JSON output"""
    import json
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        logger.warning("AI returned non-JSON format, returning raw text.")
        return {"raw": raw_text.strip()}

def now():
    """Current time in HH:MM"""
    return datetime.now().strftime("%H:%M")
