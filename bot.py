from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from dotenv import load_dotenv
import os
# Imposta il loggingfrom telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging

# Carica le variabili dal file .env
load_dotenv()

# Variabili d'ambiente
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


intro = "Benvenuto nel bot di Dolly Mitra Movies. \nQuesto bot ti permette di cercare i film che ti interessano e di ricevere l'url del file per poterli guardare. \nPer cercare un film, digita il nome del film che ti interessa."
reject = "Non sei autorizzato ad utilizzare il bot.\n"

# Imposta il logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Funzione per gestire il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.effective_chat.id

    # Messaggio di benvenuto all'utente
    message = f"Ciao {user.first_name}, benvenuto in DollyMitraMovies.\nAttendi che gli amministratori attivino il servizio per te."
    await context.bot.send_message(chat_id=chat_id, text=message)

    # Invia un messaggio all'amministratore
    await send_message_to_admin(context, user, chat_id)


# Funzione per inviare un messaggio all'amministratore
async def send_message_to_admin(context: ContextTypes.DEFAULT_TYPE, user, chat_id) -> None:
    message = f"Nuovo utente ha avviato il bot: {user.first_name} (@{user.username}, ID: {user.id})"

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
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Estrai il tipo di azione (approve/reject) e l'ID della chat dell'utente dalla callback_data
    action, chat_id = query.data.split('_')

    # Gestione della risposta in base al pulsante premuto
    if action == 'approve':
        # Invio di messaggio di approvazione all'utente
        await context.bot.send_message(chat_id=int(chat_id), text=intro)
        await query.edit_message_text(text="Utente approvato!")
        
    elif action == 'reject':
        # Invio di messaggio di rifiuto all'utente
        await context.bot.send_message(chat_id=int(chat_id), text=reject)
        await query.edit_message_text(text="Utente rifiutato!")


def main() -> None:
    application = Application.builder().token("7384437050:AAFcv89Jxysh_fmtwT5TMgew-efDglzbYQU").build()

    # Aggiunge il CommandHandler per il comando /start
    application.add_handler(CommandHandler("start", start))

    # Aggiunge il CallbackQueryHandler per gestire i pulsanti
    application.add_handler(CallbackQueryHandler(button_callback))

    # Avvia il polling per il bot
    application.run_polling()

if __name__ == "__main__":
    main()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# ID dell'amministratore
ADMIN_ID = 5767953419

# Funzione per gestire il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.effective_chat.id

    # Messaggio di benvenuto all'utente
    message = f"Ciao {user.first_name}, benvenuto in DollyMitraMovies.\nAttendi che gli amministratori attivino il servizio per te."
    await context.bot.send_message(chat_id=chat_id, text=message)

    # Invia un messaggio all'amministratore
    await send_message_to_admin(context, user, chat_id)


# Funzione per inviare un messaggio all'amministratore
async def send_message_to_admin(context: ContextTypes.DEFAULT_TYPE, user, chat_id) -> None:
    message = f"Nuovo utente ha avviato il bot: {user.first_name} (@{user.username}, ID: {user.id})"

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
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Estrai il tipo di azione (approve/reject) e l'ID della chat dell'utente dalla callback_data
    action, chat_id = query.data.split('_')

    # Gestione della risposta in base al pulsante premuto
    if action == 'approve':
        # Invio di messaggio di approvazione all'utente
        await context.bot.send_message(chat_id=int(chat_id), text=intro)
        await query.edit_message_text(text="Utente approvato!")
        
    elif action == 'reject':
        # Invio di messaggio di rifiuto all'utente
        await context.bot.send_message(chat_id=int(chat_id), text=reject)
        await query.edit_message_text(text="Utente rifiutato!")


def main() -> None:
    application = Application.builder().token("7384437050:AAFcv89Jxysh_fmtwT5TMgew-efDglzbYQU").build()

    # Aggiunge il CommandHandler per il comando /start
    application.add_handler(CommandHandler("start", start))

    # Aggiunge il CallbackQueryHandler per gestire i pulsanti
    application.add_handler(CallbackQueryHandler(button_callback))

    # Avvia il polling per il bot
    application.run_polling()

if __name__ == "__main__":
    main()
