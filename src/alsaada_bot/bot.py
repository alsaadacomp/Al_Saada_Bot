import logging
import os

from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from src.alsaada_bot.handlers.start import start
from src.alsaada_bot.handlers.menu import main_menu_callback
from src.alsaada_bot.handlers.help import help_command
from src.alsaada_bot.handlers.upload_employees import start_upload, handle_employee_upload

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def set_commands(application: Application):
    """Set the bot's commands in the Telegram UI."""
    commands = [
        BotCommand("start", "▶️ بدء البوت وعرض القائمة الرئيسية"),
        BotCommand("help", "ℹ️ عرض المساعدة"),
        BotCommand("upload_employees", "⬆️ رفع ملف الموظفين (Excel)"),
    ]
    await application.bot.set_my_commands(commands)

def run() -> None:
    """Run the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in .env file")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Set the bot's commands (the sidebar)
    application.post_init = set_commands

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("upload_employees", start_upload))
    application.add_handler(MessageHandler(filters.Document.FileExtension("xlsx"), handle_employee_upload))
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main:"))


    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    run()