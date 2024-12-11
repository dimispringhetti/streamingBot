from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import is_user_present
from streamingcommunity import StreamingCommunity
from dotenv import load_dotenv
import os
from util import reject

# variabili d'ambiente
load_dotenv()
BASE_LINK = os.getenv("BASE_LINK")

WAIT_FOR_CHOICE = 0

# Funzione per gestire il comando /search
async def command_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id

    # Se l'utente non è autorizzato manda messaggio di rifiuto
    if not is_user_present(chat_id):
        await context.bot.send_message(chat_id=chat_id, text=reject)
        return ConversationHandler.END

    # estrai il testo del messaggio
    text = update.message.text

    # rimuovi /search dal testo
    text = text.replace("/search", "").strip()

    # se il testo è vuoto, invia un messaggio di errore
    if not text:
        await context.bot.send_message(chat_id=chat_id, text="Inserisci il nome del film che vuoi cercare. (es. /search Deadpool)")
        return ConversationHandler.END

    # ricerca dei film
    sc = StreamingCommunity(BASE_LINK)
    titles = sc.search(text)

    # se non ci sono risultati
    if not titles:
        await context.bot.send_message(chat_id=chat_id, text="Nessun risultato trovato. Riprova con un altro titolo.")
        return ConversationHandler.END

    # salva i titoli trovati nel contesto dell'utente
    context.user_data["titles"] = titles

    # creo il messaggio con i film (1. Deadpool)
    titles_namelists = "\n".join([f"{i}. {title.get().name}" for i, title in enumerate(titles, start=1)])
    message = f"Risultati della ricerca: \n{titles_namelists}\nRispondi con il numero del film che vuoi scegliere. Per uscire digita 0"
    await context.bot.send_message(chat_id=chat_id, text=message)

    return WAIT_FOR_CHOICE


# Gestione risposta
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    user_choice = update.message.text

    titles = context.user_data.get("titles", [])

    # Verifica se l'input è un numero
    if not user_choice.isnumeric():
        await context.bot.send_message(chat_id=chat_id, text="Scrivi un numero. Riprova.")
        return WAIT_FOR_CHOICE

    choice = int(user_choice)

    # Se l'utente sceglie 0, termina la conversazione
    if choice == 0:
        await context.bot.send_message(chat_id=chat_id, text="Conversazione terminata.")
        return ConversationHandler.END

    # Controllo se è fuori range
    if choice < 1 or choice > len(titles):
        await context.bot.send_message(chat_id=chat_id, text="Scelta fuori dal range. Riprova.")
        return WAIT_FOR_CHOICE

    if choice == 0:
        return 0

    # Ottieni il titolo selezionato e invia conferma
    selected = titles[choice - 1].get()
    await context.bot.send_message(chat_id=chat_id, text=f"{selected.name}: {selected.playlist_url}")
    return ConversationHandler.END
