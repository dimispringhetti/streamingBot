from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os
from database import add_user, is_user_not_approved, is_user_present, add_not_approved
from util import intro, reject, still_present
import logging

# Carica le variabili dal file .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Funzione per gestire il comando /start
async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.effective_chat.id

    # fix richieste multiple:
    # Se l'utente è già presente tra i non approvati, invia un messaggio di rifiuto
    if is_user_not_approved(chat_id):
        await context.bot.send_message(chat_id=chat_id, text=reject)
        return
    # Se l'utente è già presente tra gli utenti, invia un messaggio di benvenuto
    if is_user_present(chat_id):
        await context.bot.send_message(chat_id=chat_id, text=still_present)
        return

    # Messaggio di benvenuto all'utente
    message = f"Ciao {user.first_name}, benvenuto in DollyMitraMovies.\nAttendi che gli amministratori attivino il servizio per te."
    await context.bot.send_message(chat_id=chat_id, text=message)

    # Invia un messaggio all'amministratore
    await send_message_to_admin(context, user, chat_id)


# Funzione per inviare un messaggio all'amministratore
async def send_message_to_admin(context: ContextTypes.DEFAULT_TYPE, user, chat_id) -> None:
    message = f"Nuovo utente ha avviato il bot: {user.first_name} (@{user.username}, ID: {chat_id})"

    # Tastiera con approvazione o rifiuto, includendo l'ID della chat dell'utente nella callback_data
    keyboard = [
        [InlineKeyboardButton("Approva", callback_data=f'approve_{chat_id}')],
        [InlineKeyboardButton("Rifiuta", callback_data=f'reject_{chat_id}')],
    ]

    # Creazione della tastiera
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Invia il messaggio all'amministratore
    await context.bot.send_message(chat_id=ADMIN_ID, text=message, reply_markup=reply_markup)


# Funzione per gestire la scelta dell'amministratore
async def button_approve_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Estrai il tipo di azione (approve/reject) e l'ID della chat dell'utente dalla callback_data
    action, chat_id = query.data.split('_')

    # Gestione della risposta in base al pulsante premuto
    if action == 'approve':
        # Aggiungi l'utente alla lista degli utenti
        await add_user(int(chat_id), query.from_user.username, query.from_user.first_name)
        # Invio di messaggio di benvenuto all'utente
        await context.bot.send_message(chat_id=int(chat_id), text=intro)
        # Invio di messaggio di approvazione all'admin
        await query.edit_message_text(text="Utente approvato!")

    elif action == 'reject':
        # Aggiungi l'utente alla lista degli utenti non approvati
        await add_not_approved(int(chat_id), query.from_user.username, query.from_user.first_name)
        # Invio di messaggio di rifiuto all'utente
        await context.bot.send_message(chat_id=int(chat_id), text=reject)
        # Invio di messaggio di rifiuto all'admin
        await query.edit_message_text(text="Utente rifiutato!")

