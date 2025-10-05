# Placeholder for database connection
# Later you can connect SQLite/PostgreSQL
def get_affirmations():
    return [
        "Ты делаешь огромный шаг вперёд 🌟",
        "Любовь — это терапия 💚",
        "Ты создаёшь стабильность для своего ребёнка 🌱",
        "Замечай маленькие улучшения каждый день ✨"
    ]

# Placeholder diary storage
diary_storage = {}

def add_diary_entry(user_id, entry):
    if user_id not in diary_storage:
        diary_storage[user_id] = []
    diary_storage[user_id].append(entry)

def get_diary(user_id):
    return diary_storage.get(user_id, [])
