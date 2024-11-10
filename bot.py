from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from dotenv import load_dotenv
import os
from search import command_search
from new_user import command_start, button_approve_callback

# Carica le variabili dal file .env
load_dotenv()

# Variabili d'ambiente
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Imposta il logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Aggiunge il CommandHandler per i comandi
    application.add_handler(CommandHandler("start", command_start))
    application.add_handler(CommandHandler("search", command_search))

    # Aggiunge il CallbackQueryHandler per gestire i pulsanti
    application.add_handler(CallbackQueryHandler(button_approve_callback))

    # Avvia il polling per il bot
    application.run_polling()

if __name__ == "__main__":
    main()
