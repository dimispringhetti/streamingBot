import requests
import urllib.parse
import re
from typing import Tuple
from dotenv import load_dotenv
import os
from database import is_user_present
from telegram import Update
from telegram.ext import CallbackContext
from util import reject

# Carica le variabili dal file .env
load_dotenv()

base_link = os.getenv("BASE_LINK")
search_endpoint = "/search"
title_endpoint = "/titles"

def get_inertia_version(url: str) -> str | None:
    pattern = r"version&quot;:&quot;([a-f0-9]+)&quot;"
    try:
        res = requests.get(url)
        _match = re.search(pattern, res.text)
        if _match:
            return _match.group(1)
        else:
            return None
    except:
        return None

def search_titles(query: str) -> list[dict] | None:
    params = {"q": query}
    url = f"{base_link}{search_endpoint}?{urllib.parse.urlencode(params)}"
    try:
        inertia_version = get_inertia_version(url)
        res = requests.get(url,
            headers={
                "X-Inertia": "true",
                "X-Inertia-Version": inertia_version
            }
        )
        return res.json()['props']['titles']
    except:
        return None

def get_title_info(id: int, slug: str) -> Tuple[dict, str] | None:
    url = f"{base_link}{title_endpoint}/{id}-{slug}"
    try:
        inertia_version = get_inertia_version(url)
        res = requests.get(url,
            headers={
                "X-Inertia": "true",
                "X-Inertia-Version": inertia_version
            }
        )
        props = res.json()['props']
        playlist_url = f"{props['scws_url']}/playlist/{props['title']['scws_id']}"
        return (props, playlist_url)
    except:
        return None

def search_movie(name: str) -> str:
    titles = search_titles(name)
    if titles:
        title = titles[0]
        id = title['id']
        slug = title['slug']
        (props, playlist) = get_title_info(id, slug) or (None, None)
        return playlist
    return None

# comando search
async def command_search(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    # non autorizzato
    if not is_user_present(chat_id):
        await context.bot.send_message(chat_id=chat_id, text=reject)
        return

    # estrai il testo del messaggio
    text = update.message.text
    # rimuovi /search dal testo
    text = text.replace("/search", "")

    # se il testo è vuoto, invia un messaggio di errore
    if not text:
        await context.bot.send_message(chat_id=chat_id, text="Inserisci il nome del film che vuoi cercare. (es. /search Deadpool)")
        return
    
    # cerca il film
    result = search_movie(text)

    if result == None:
        ans = "Film non trovato."
    else:
        ans = result

    # invia il risultato della ricerca
    await context.bot.send_message(chat_id=chat_id, text=f"Codice del film: {ans}")
