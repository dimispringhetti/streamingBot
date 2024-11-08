import json

# Carica utenti
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # lista vuota se il file non esiste

def load_not_approved():
    try:
        with open("not_approved.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # lista vuota se il file non esiste

# Salva utenti non approvati nel file JSON
def save_not_approved(not_approved):
    with open("not_approved.json", "w") as file:
        json.dump(not_approved, file, indent=4)

# Salva utenti nel file JSON
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# Controllo se l'utente è già presente
def is_user_present(user_id):
    users = load_users()
    return any(user['ID'] == user_id for user in users)

# Funzione per aggiungere un utente
async def add_user(user_id, username, first_name):
    users = load_users()
    users.append({
        "ID": user_id,
        "USERNAME": username,
        "FIRST_NAME": first_name
    })
    save_users(users)

# Funzione per aggiungere un utente non approvato
async def add_not_approved(user_id, username, first_name):
    not_approved = load_not_approved()
    not_approved.append({
        "ID": user_id,
        "USERNAME": username,
        "FIRST_NAME": first_name
    })
    save_not_approved(not_approved)


# Funzione per controllare se l'utente è già tra i non approvati
def is_user_not_approved(user_id):
    not_approved = load_not_approved()
    return any(user['ID'] == user_id for user in not_approved)

# Funzione per controllare se l'utente è già tra gli users
def is_user_present(user_id):
    users = load_users()
    return any(user['ID'] == user_id for user in users)