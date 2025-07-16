import logging
from telegram import Update
from telegram.ext import ContextTypes

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة الضغط على أزرار القائمة الرئيسية."""
    query = update.callback_query
    await query.answer()  # ضروري للرد على تيليجرام بأن الضغطة استُلمت

    selected_option = query.data.split(":")[1]
    logging.info(f"User {query.from_user.first_name} selected '{selected_option}' from main menu.")

    # تعديل الرسالة الأصلية لعرض رسالة "قيد التطوير"
    # هذا يطبق مبدأ تفعيل الوظائف تدريجياً
    await query.edit_message_text(
        text=f'قسم "{selected_option}" قيد التطوير حاليًا. ترقب التحديثات القادمة! 🛠️'
    )
