from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from search import WAIT_FOR_CHOICE, command_search, handle_choice
from dotenv import load_dotenv
import os
from new_user import command_start, button_approve_callback
import logging

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
    # Crea l'applicazione del bot
    application = Application.builder().token(TOKEN).build()

    # Aggiunge il CommandHandler per i comandi
    application.add_handler(CommandHandler("start", command_start))

    # Aggiunge il ConversationHandler per /search
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("search", command_search)],
        states={
            WAIT_FOR_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
        },
        fallbacks=[],
    )

    # Aggiunge il CallbackQueryHandler per gestire i pulsanti
    application.add_handler(CallbackQueryHandler(button_approve_callback))
    application.add_handler(conv_handler)  # /search

    # Avvia il polling per il bot
    application.run_polling()

if __name__ == "__main__":
    main()
