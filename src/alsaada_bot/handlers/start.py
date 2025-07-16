import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# --- Main Menu Definition ---
# This list is based on the project documentation and user requirements
MAIN_MENU_STRUCTURE = {
    "شؤون الموظفين": {
        "icon": "👥",
        "sub_menu": {
            "قائمة الموظفين": {"icon": "📄", "callback": "employees:list"},
            "الرواتب والسلف": {"icon": "💰", "callback": "salaries:main"},
            "الحضور والإجازات": {"icon": "⏰", "callback": "attendance:main"},
        }
    },
    "الحسابات": {
        "icon": "📊",
        "sub_menu": {
            "المصروفات": {"icon": "💸", "callback": "expenses:main"},
            "الإيرادات": {"icon": "📈", "callback": "revenues:main"},
            "العهد": {"icon": "💼", "callback": "custodies:main"},
            "الموردين": {"icon": "🤝", "callback": "suppliers:main"},
            "حسابات المقاولين": {"icon": "🏗️", "callback": "contractors:main"},
        }
    },
    "الصيانة والتشغيل": {
        "icon": "🛠️",
        "sub_menu": {
            "مخزون الزيوت وقطع الغيار": {"icon": "🛢️", "callback": "stock:main"},
            "عمليات الصيانة": {"icon": "🔧", "callback": "maintenance:main"},
            "التشغيل اليومي": {"icon": "🗓️", "callback": "daily_ops:main"},
            "المعدات المستأجرة": {"icon": "🚜", "callback": "rented_eq:main"},
        }
    },
    "ملاحظات وتاسكات": {"icon": "📝", "callback": "notes:main"},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with the main menu when the /start command is issued."""
    user = update.effective_user
    logging.info(f"User {user.first_name} ({user.id}) started the bot.")

    keyboard = []
    for main_item, details in MAIN_MENU_STRUCTURE.items():
        if "sub_menu" in details:
            # Main categories with sub-menus
            keyboard.append([InlineKeyboardButton(f"{details["icon"]} {main_item}", callback_data=f"menu:{main_item}")])
        else:
            # Direct items like "Notes and Tasks"
            keyboard.append([InlineKeyboardButton(f"{details["icon"]} {main_item}", callback_data=details["callback"])])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_html(
        rf"مرحباً بك يا {user.mention_html()} في بوت السعادة للمقاولات!",
        reply_markup=reply_markup,
    )

async def show_sub_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, menu_key: str) -> None:
    """Displays a sub-menu based on the selected main category."""
    query = update.callback_query
    await query.answer()

    sub_menu_items = MAIN_MENU_STRUCTURE.get(menu_key, {}).get("sub_menu", {})
    keyboard = []
    for item_name, item_details in sub_menu_items.items():
        keyboard.append([InlineKeyboardButton(f"{item_details["icon"]} {item_name}", callback_data=item_details["callback"])])

    # Add a back button
    keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="menu:main_back")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"اختر من قائمة {menu_key}:",
        reply_markup=reply_markup,
    )