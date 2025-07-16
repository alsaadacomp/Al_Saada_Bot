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
        },
    },
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
            # FIX: Broke the long key-value pair into multiple lines
            "مخزون الزيوت وقطع الغيار": {
                "icon": "🛢️",
                "callback": "stock:main",
            },
            "عمليات الصيانة": {"icon": "🔧", "callback": "maintenance:main"},
            "التشغيل اليومي": {"icon": "🗓️", "callback": "daily_ops:main"},
            "المعدات المستأجرة": {"icon": "🚜", "callback": "rented_eq:main"},
        },
    },
    "ملاحظات وتاسكات": {"icon": "📝", "callback": "notes:main"},
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # FIX: Broke the long docstring into multiple lines
    """
    Sends a welcome message with the main menu when the /start command is issued.
    """
    user = update.effective_user
    logging.info(f"User {user.first_name} ({user.id}) started the bot.")

    # The complex list comprehension was replaced with a standard for-loop.
    # This is more readable, easier to maintain, and fixes parsing issues
    # for tools like 'black'.
    keyboard = []
    for main_item, details in MAIN_MENU_STRUCTURE.items():
        # Check if the menu item has a sub-menu
        if "sub_menu" in details:
            # FIX: Broke the long function call into multiple lines
            button = InlineKeyboardButton(
                f"{details['icon']} {main_item}",
                callback_data=f"menu:{main_item}",
            )
        # Otherwise, it's a direct action item
        else:
            # FIX: Broke the long function call into multiple lines
            button = InlineKeyboardButton(
                f"{details['icon']} {main_item}",
                callback_data=details["callback"],
            )
        keyboard.append([button])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_html(
        rf"مرحباً بك يا {user.mention_html()} في بوت السعادة للمقاولات!",
        reply_markup=reply_markup,
    )


async def show_sub_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE, menu_key: str
) -> None:
    """Displays a sub-menu based on the selected main category."""
    query = update.callback_query
    await query.answer()

    sub_menu_items = MAIN_MENU_STRUCTURE.get(menu_key, {}).get("sub_menu", {})
    keyboard = []
    for item_name, item_details in sub_menu_items.items():
        button = InlineKeyboardButton(
            f"{item_details['icon']} {item_name}",
            callback_data=item_details["callback"],
        )
        keyboard.append([button])

    # Add a back button
    # FIX: Broke the long function call into multiple lines
    back_button = InlineKeyboardButton(
        "🔙 رجوع للقائمة الرئيسية", callback_data="menu:main_back"
    )
    keyboard.append([back_button])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"اختر من قائمة {menu_key}:",
        reply_markup=reply_markup,
    )
