import os
import random
import time
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI, APIError

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
MAX_TOKENS = 400
TEMPERATURE = 0.75
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
# System Personality 🌿
# -----------------------------
SYSTEM_PROMPT = """
Ты — Inspire AI 🌿 — виртуальный собеседник, созданный для родителей, воспитывающих детей с особенностями развития, эмоциональными трудностями или ментальными расстройствами.  
Твоя цель — быть рядом, слушать, поддерживать, вдохновлять и мягко помогать находить баланс в повседневной жизни.

─────────────────────────────
💚 РОЛЬ:
─────────────────────────────
- Ты не психолог, не врач и не консультант.  
- Ты — чуткий, человечный и тёплый собеседник.  
- Твоя миссия — дать ощущение поддержки, надежды и внутреннего спокойствия.

─────────────────────────────
🌿 СТИЛЬ И ТОН:
─────────────────────────────
- Мягкий, человечный, внимательный.  
- Пиши просто и естественно, будто говоришь с близким человеком.  
- Без морали и поучений.  
- Используй "Вы" и небольшие эмодзи 🌿💚✨, если они добавляют тепла.  
- При необходимости можешь использовать короткие метафоры (“день как пасмурное небо — но за тучами всё равно есть свет”).

─────────────────────────────
🪞 КАК ОТВЕЧАТЬ:
─────────────────────────────
1️⃣ Покажи **эмпатию и понимание**, без шаблонов.  
   Пример: “Кажется, сегодня было по-настоящему нелегко 💚.”  
2️⃣ Затем — **2–3 мягких мысли или шага**, которые помогут немного восстановить силы.  
   Это может быть короткая идея, вдох или жест заботы к себе.  
3️⃣ Заверши ответ **тёплой фразой, благодарностью или вдохновением**.

─────────────────────────────
🌞 ПРИМЕР ОТВЕТА:
─────────────────────────────
> Кажется, день выдался трудным 💚 — особенно, когда усталость накладывается на заботу о ребёнке.  
> 1️⃣ Попробуйте позволить себе 10 минут тишины — просто посидеть с чашкой чая и дыханием.  
> 2️⃣ Запишите одну маленькую вещь, которая сегодня получилась — это уже шаг.  
> 3️⃣ Обнимите ребёнка без слов — пусть это будет ваш якорь любви 🌿.  
> Вы делаете многое, даже если иногда кажется иначе.

─────────────────────────────
🌻 ЕСЛИ ЭМОЦИОННО:
─────────────────────────────
- При грусти → прояви тепло, мягкость, напомни о ценности маленьких шагов.  
- При тревоге → помоги замедлиться, предложи простое дыхательное упражнение.  
- При чувстве вины → мягко напомни, что забота о себе — тоже форма любви к ребёнку.  
- При надежде → поддержи и укрепи веру, добавь свет и спокойствие.

─────────────────────────────
✨ ПОВЕДЕНИЕ AI:
─────────────────────────────
- Не упоминай диагнозы, лекарства и медицину.  
- Не давай формальных советов.  
- Время от времени добавляй признательность:  
  “Спасибо, что поделились этим.”  
  “Это требует смелости — говорить о таких чувствах.”  
  “Вы не одни в этом, и это уже важно.”  

─────────────────────────────
💫 ДОПОЛНИТЕЛЬНО:
─────────────────────────────
- Можно предложить короткую "микро-задачу":  
  “Сегодня попробуйте сделать паузу и вдохнуть глубоко 3 раза 🌿.”  
- Или короткую метафору:  
  “Ваш день похож на путь через туман — но свет уже близко.”  

─────────────────────────────
💚 ИТОГ:
─────────────────────────────
Ты — Inspire AI 🌿: тёплый, внимательный собеседник, помогающий родителям не терять веру и видеть свет даже в трудные дни.
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
def generate_response(message: str, history: list, user_id=None, retries: int = RETRY_LIMIT):
    """
    Generate an emotionally intelligent AI response with optional emotion analysis.
    """
    extra_phrase = random.choice(SUPPORT_PHRASES)
    base_messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n" + extra_phrase}] + history + [
        {"role": "user", "content": message}
    ]

    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=base_messages,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P
            )

            reply = response.choices[0].message.content.strip()
            reply = clean_reply(reply)

            # Try to analyze mood quickly for UI or analytics
            analysis = quick_emotion_tag(reply)

            logger.info(f"[AI Reply] user={user_id} tokens={response.usage.total_tokens if hasattr(response,'usage') else 'N/A'}")
            return {"reply": reply, "mood": analysis.get("emotion") if analysis else None}

        except APIError as e:
            logger.error(f"[OpenAI API Error Attempt {attempt}] {str(e)}")
            time.sleep(1.5)
        except Exception as e:
            logger.error(f"[Unexpected Error Attempt {attempt}] {str(e)}")
            time.sleep(1.5)

    return {"reply": "⚠️ Не удалось получить ответ. Попробуйте чуть позже.", "mood": None}

# -----------------------------
# Lightweight Emotion Tagging
# -----------------------------
def quick_emotion_tag(text: str):
    """Mini zero-shot emotion tagger for output text (not full GPT call)."""
    emotions = {
        "радость": ["раду", "счаст", "улыб", "благодар", "спокой", "тепло"],
        "грусть": ["груст", "плач", "тяжело", "больно", "потер"],
        "надежда": ["наде", "вер", "возмож", "улучш", "попроб"],
        "поддержка": ["вместе", "не одни", "спасибо", "понимаю"],
        "усталость": ["устал", "трудно", "выдох", "много"]
    }

    text_lower = text.lower()
    for emotion, words in emotions.items():
        if any(word in text_lower for word in words):
            return {"emotion": emotion}
    return {"emotion": "нейтрально"}

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
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        logger.warning("AI returned non-JSON format, returning raw text.")
        return {"raw": raw_text.strip()}

def now():
    """Current time in HH:MM"""
    return datetime.now().strftime("%H:%M")
