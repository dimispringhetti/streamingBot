import json

# Carica utenti
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # lista vuota se il file non esiste

# Salva utenti nel file JSON
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# ìControllo se l'utente è già presente
def is_user_present(user_id):
    users = load_users()
    return any(user['ID'] == user_id for user in users)

# Funzione per aggiungere un utente
async def add_user(user_id, username, first_name):
    users = load_users()
    # Controlla se l'utente è già presente
    if is_user_present(user_id):
        return False
    else:
        users.append({
            "ID": user_id,
            "USERNAME": username,
            "FIRST_NAME": first_name
        })
        save_users(users)
        return True
