from telegram.ext import ApplicationBuilder, CommandHandler
from database import init_db
from commands import start, balance, send, help_command
from config import BOT_TOKEN


def main():
    init_db()  # Initialize the database

    # Replace 'YOUR_API_TOKEN' with your bot's API token
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("send", send))
    application.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
