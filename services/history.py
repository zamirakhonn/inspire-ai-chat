# Simple in-memory history for demo; can switch to DB
chat_histories = {}

def get_chat_history(user_id):
    return chat_histories.get(user_id, [])

def add_to_history(user_id, role, content):
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    chat_histories[user_id].append({"role": role, "content": content})
