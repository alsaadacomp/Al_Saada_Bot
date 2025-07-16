# المسار: src/alsaada_bot/handlers/start.py
# الرجاء استبدال محتوى الملف بالكامل بهذا الكود

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# --- تعريف هيكل القائمة الرئيسية الكامل ---
MAIN_MENU_STRUCTURE = {
    "شؤون الموظفين": {"icon": "👥", "callback": "employees:main"},
    "الحسابات": {
        "icon": "📊",
        "sub_menu": {
            "المصروفات": {"icon": "💸", "callback": "expenses:main"},
            "الإيرادات": {"icon": "📈", "callback": "revenues:main"},
            "العهد": {"icon": "💼", "callback": "custodies:main"},
            "الموردين": {"icon": "🤝", "callback": "suppliers:main"},
            "حسابات المقاولين": {"icon": "🏗️", "callback": "contractors:main"},
        },
    },
    "الصيانة والتشغيل": {
        "icon": "🛠️",
        "sub_menu": {
            "مخزون الزيوت وقطع الغيار": {"icon": "🛢️", "callback": "stock:main"},
            "عمليات الصيانة": {"icon": "🔧", "callback": "maintenance:main"},
            "التشغيل اليومي": {"icon": "🗓️", "callback": "daily_ops:main"},
            "المعدات المستأجرة": {"icon": "🚜", "callback": "rented_eq:main"},
        },
    },
    "ملاحظات وتاسكات": {"icon": "📝", "callback": "notes:main"},
}


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    تقوم ببناء وإرجاع لوحة المفاتيح للقائمة الرئيسية.
    """
    keyboard = []
    for main_item, details in MAIN_MENU_STRUCTURE.items():
        if "callback" in details:
            button = InlineKeyboardButton(
                f"{details['icon']} {main_item}", callback_data=details["callback"]
            )
        elif "sub_menu" in details:
            button = InlineKeyboardButton(
                f"{details['icon']} {main_item}", callback_data=f"menu:show:{main_item}"
            )
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    ترسل رسالة ترحيبية مع القائمة الرئيسية عند استدعاء أمر /start.
    """
    user = update.effective_user
    logging.info(f"User {user.first_name} ({user.id}) started the bot.")

    reply_markup = get_main_menu_keyboard()
    await update.message.reply_html(
        rf"مرحباً بك يا {user.mention_html()} في بوت السعادة للمقاولات!",
        reply_markup=reply_markup,
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    تقوم بتعديل الرسالة الحالية لعرض القائمة الرئيسية (تستخدم لزر الرجوع).
    """
    query = update.callback_query
    reply_markup = get_main_menu_keyboard()
    await query.edit_message_text(text="القائمة الرئيسية:", reply_markup=reply_markup)


async def show_sub_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE, menu_key: str
) -> None:
    """
    تعرض القائمة الفرعية البسيطة بناءً على الفئة الرئيسية التي تم اختيارها.
    """
    query = update.callback_query
    sub_menu_items = MAIN_MENU_STRUCTURE.get(menu_key, {}).get("sub_menu", {})

    if not sub_menu_items:
        await query.edit_message_text(text="خطأ: القائمة الفرعية غير موجودة.")
        return

    keyboard = []
    for item_name, item_details in sub_menu_items.items():
        button = InlineKeyboardButton(
            f"{item_details['icon']} {item_name}",
            callback_data=item_details["callback"],
        )
        keyboard.append([button])

    back_button = InlineKeyboardButton("🔙 رجوع", callback_data="menu:back_to_main")
    keyboard.append([back_button])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"اختر من قائمة {menu_key}:",
        reply_markup=reply_markup,
    )
