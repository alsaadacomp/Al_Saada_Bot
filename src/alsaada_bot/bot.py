# المسار: src/alsaada_bot/bot.py
# الرجاء استبدال محتوى الملف بالكامل بهذا الكود

import logging
import os

from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# استيراد المعالجات من ملفاتها الصحيحة
from src.alsaada_bot.handlers.employees import show_employees_menu
from src.alsaada_bot.handlers.help import help_command
from src.alsaada_bot.handlers.start import (
    show_main_menu,
    show_sub_menu,
    start_command,
)
from src.alsaada_bot.handlers.upload_employees import (
    handle_employee_upload,
    start_upload,
)

# تفعيل تسجيل الأنشطة
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """يعالج جميع الضغطات على أزرار القوائم."""
    query = update.callback_query
    await query.answer()

    # callback_data format: "type:action:value"
    # Examples: "menu:back_to_main", "menu:show:الحسابات", "employees:main"
    parts = query.data.split(":", 2)
    menu_type = parts[0]
    action = parts[1] if len(parts) > 1 else ""
    value = parts[2] if len(parts) > 2 else ""

    if menu_type == "menu":
        if action == "back_to_main":
            await show_main_menu(update, context)
        elif action == "show":
            await show_sub_menu(update, context, menu_key=value)

    elif menu_type == "employees":
        if action == "main":
            await show_employees_menu(update, context)
        else:
            # سيتم إضافة منطق باقي وظائف الموظفين هنا
            await query.edit_message_text(
                text=f"وظيفة الموظفين ({action}) قيد الإنشاء."
            )

    else:
        # معالجة أنواع القوائم الأخرى (ملاحظات، مصروفات، الخ)
        await query.edit_message_text(
            text=f"تم اختيار: {query.data}\n\n(الوظيفة قيد الإنشاء)"
        )


async def set_commands(application: Application):
    """تحديد الأوامر التي تظهر في قائمة تليجرام."""
    commands = [
        BotCommand("start", "▶️ بدء البوت وعرض القائمة الرئيسية"),
        BotCommand("help", "ℹ️ عرض المساعدة"),
        BotCommand("upload_employees", "⬆️ رفع ملف الموظفين (Excel)"),
    ]
    await application.bot.set_my_commands(commands)


def run() -> None:
    """تشغيل البوت."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in .env file")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.post_init = set_commands

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("upload_employees", start_upload))
    application.add_handler(
        MessageHandler(filters.Document.FileExtension("xlsx"), handle_employee_upload)
    )

    # هذا المعالج الشامل هو المسؤول عن كل الأزرار
    application.add_handler(CallbackQueryHandler(main_menu_callback))

    logger.info("Bot is running...")
    application.run_polling()
