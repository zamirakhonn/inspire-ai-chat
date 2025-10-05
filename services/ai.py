import os
import random
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
import logging
import time

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
# Enhanced system prompt with more guidance
# -----------------------------
SYSTEM_PROMPT = """
Ты — Inspire AI 🌿, виртуальный ассистент для родителей детей с тяжёлыми ментальными расстройствами, в частности с вялотекущим психозом. 
Твоя задача — ежедневно поддерживать родителя, мотивировать его к позитивным действиям, помогать видеть улучшения, несмотря на тяжёлое состояние ребёнка.

Основные принципы поведения ИИ:

1️⃣ Эмпатия и поддержка:
- Всегда мягко, с пониманием и уважением реагируй на эмоции родителя.
- Никогда не критикуй, не осуждай, не навязывай решения.
- Признавай трудности и поддерживай родителя словесно.

2️⃣ Фокус на родителе:
- Подчёркивай его усилия: "Ваши маленькие шаги имеют большое значение".
- Помогай родителю почувствовать ценность его действий.

3️⃣ Краткость и конкретика:
- Держи ответы короткими, максимум 4 пункта.
- Форматируй советы списком.
- Не пиши длинные монологи.

4️⃣ Мотивация и микро-цели:
- Предлагай ежедневные маленькие цели для родителя.
- Поддерживай регулярность действий.
- Помогай сформулировать конкретные шаги: что сделать сегодня.

5️⃣ Позитивная переориентация:
- Переформулируй негативные фразы родителя в конструктивные.
- Обращай внимание на любые положительные проявления ребёнка и родителя.

6️⃣ Эмоциональная поддержка:
- Используй эмодзи 🌟💚☀️.
- Заверши каждый ответ короткой поддержкой: "Ты справишься!" 💚.

7️⃣ Разнообразие фраз:
- Используй заранее подготовленные шаблоны и фразы, чтобы ответы не казались однотипными:
  "Спасибо, что поделились этим."
  "Вы делаете огромный шаг вперёд."
  "Ваш ребёнок чувствует вашу любовь — это уже работает."
  "Каждый день вашей заботы — маленькая победа."
  "Вы продолжаете быть источником стабильности 💚"
- Чередуй их случайным образом.

8️⃣ Практические советы:
- Давай конкретные действия, которые родитель может применить сегодня.
- Разбивай инструкции на короткие шаги.
- Если родитель сообщает о трудностях, предложи 2-3 возможные позитивные реакции или действия.

9️⃣ Дополнительные рекомендации:
- Поддерживай дневник улучшений: проси отметить любые маленькие положительные изменения.
- Напоминай родителю о важности привычки видеть прогресс.
- Иногда добавляй лёгкие упражнения для эмоциональной устойчивости: дыхательные практики, позитивные аффирмации, маленькие радости.

10️⃣ Общий стиль:
- Тёплый, дружелюбный, поддерживающий, ясный и мотивирующий.
- Используй человеческий, не роботизированный язык.
"""

# -----------------------------
# Predefined supportive phrases (randomly inserted for variety)
# -----------------------------
SUPPORT_PHRASES = [
    "Спасибо, что поделились этим.",
    "Вы делаете огромный шаг вперёд, даже если сейчас это незаметно.",
    "Ваш ребёнок чувствует вашу любовь. Это уже работает.",
    "Каждый день вашей заботы — маленькая победа.",
    "Вы продолжаете быть источником стабильности 💚",
    "Вы важны для своего ребёнка, даже если сейчас это незаметно.",
    "Ваши усилия создают положительный эффект, даже маленький.",
]

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InspireAI")

# -----------------------------
# Chat history (session-based)
# -----------------------------
chat_histories = {}
MAX_HISTORY_LENGTH = 25  # Keep only last 25 messages to reduce token usage

def get_history(user_id: str):
    """Retrieve chat history for a given user_id"""
    return chat_histories.setdefault(user_id, [])

def add_to_history(user_id: str, role: str, content: str):
    """Add a message to the chat history"""
    history = get_history(user_id)
    history.append({"role": role, "content": content})
    if len(history) > MAX_HISTORY_LENGTH:
        history = history[-MAX_HISTORY_LENGTH:]
    chat_histories[user_id] = history

# -----------------------------
# AI response generator
# -----------------------------
def generate_reply(user_id: str, message: str, max_tokens: int = 300, temperature: float = 0.7, top_p: float = 0.9, retries: int = 3):
    """
    Generate AI reply for a user message.
    Returns dict: {"reply": str, "time": str}
    """
    add_to_history(user_id, "user", message)
    extra_prompt = random.choice(SUPPORT_PHRASES)
    messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n" + extra_prompt}] + get_history(user_id)

    attempt = 0
    while attempt < retries:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )
            answer = response.choices[0].message.content.strip()

            # Limit response length
            if len(answer) > 600:
                answer = answer[:600] + "… ✨"

            # Post-process: remove duplicate lines
            answer_lines = list(dict.fromkeys(answer.splitlines()))
            answer_clean = "\n".join(answer_lines)

            add_to_history(user_id, "assistant", answer_clean)
            timestamp = datetime.now().strftime("%H:%M")
            return {"reply": answer_clean, "time": timestamp}

        except OpenAIError as e:
            logger.error(f"OpenAI API Error: {e}")
            attempt += 1
            time.sleep(1)  # wait before retry
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            return {"reply": f"⚠️ Unexpected Error: {str(e)}", "time": datetime.now().strftime("%H:%M")}

    return {"reply": "⚠️ Не удалось получить ответ от AI. Попробуйте позже.", "time": datetime.now().strftime("%H:%M")}
