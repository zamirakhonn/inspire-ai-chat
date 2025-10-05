# In-memory user storage
users = {}

def register_user(username, password):
    if username in users:
        return False
    users[username] = password
    return True

def check_credentials(username, password):
    return users.get(username) == password
