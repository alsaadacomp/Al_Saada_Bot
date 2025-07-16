import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.alsaada_bot.handlers.start import MAIN_MENU_STRUCTURE, show_sub_menu, start

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button presses from the main menu and sub-menus."""
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    callback_data = query.data
    logging.info(f"User {query.from_user.first_name} selected '{callback_data}'.")

    if callback_data.startswith("menu:"):
        menu_key = callback_data.split(":")[1]
        if menu_key == "main_back":
            await start(update, context) # Go back to main menu
        else:
            # It's a main category, show its sub-menu
            await show_sub_menu(update, context, menu_key)
    else:
        # It's a specific function, currently under development
        await query.edit_message_text(
            text=f"هذه الوظيفة قيد التطوير حاليًا. ترقب التحديثات القادمة! 🛠️"
        )