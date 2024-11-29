from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from database import is_user_present
from util import intro, reject, still_present
from streamingcommunity import StreamingCommunity
from dotenv import load_dotenv
import os

# variabili d'ambiente
load_dotenv()
BASE_LINK = os.getenv("BASE_LINK")

# Funzione per gestire il comando /search
async def command_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    # Se l'utente non è autorizzato manda messaggio di rifiuto
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
    
    # ricerca dei film
    sc = StreamingCommunity(BASE_LINK)
    titles = sc.search(text)
   
    titles_namelists = ""
    count = 0
    for title in titles:
        count += 1
        titles_namelists += f"{count}. {title.get().name}\n"

    message = "Risultati della ricerca: \n" + titles_namelists
    await context.bot.send_message(chat_id=chat_id, text=message)

    #await choice(chat_id, text)    

'''
# Funzione per scegliere il film
async def choice(context: ContextTypes.DEFAULT_TYPE, chat_id, searched_title) -> None:


    # Tastiera con selezione dei film, includendo l'ID della chat dell'utente nella callback_data
    keyboard = [
        [InlineKeyboardButton("1", callback_data=f'1_{chat_id}'), InlineKeyboardButton("2", callback_data=f'2_{chat_id}')],
        [InlineKeyboardButton("<", callback_data=f'forward_{chat_id}'), InlineKeyboardButton(">", callback_data=f'back_{chat_id}')],
    ]

    # Creazione della tastiera
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Invia il messaggio all'utente
    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


# Funzione per gestire la scelta dell'utente
async def button_search_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Estrai il tipo di azione (1 o 2) e l'ID della chat dell'utente dalla callback_data
    action, chat_id = query.data.split('_')

    # Gestione della risposta in base al pulsante premuto
    if action == '1':
        # Invio di messaggio di benvenuto all'utente
        await context.bot.send_message(chat_id=int(chat_id), text=intro)
        # Invio di messaggio di approvazione all'admin
        await query.edit_message_text(text="")

    elif action == '2':
        # Invio di messaggio di rifiuto all'utente
        await context.bot.send_message(chat_id=int(chat_id), text=reject)
        # Invio di messaggio di rifiuto all'admin
        await query.edit_message_text(text="")

'''