from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# --- تعريف هيكل قائمة الموظفين ---
EMPLOYEES_MENU_STRUCTURE = {
    "add_employee": {"icon": "➕", "text": "إضافة موظف جديد"},
    "list_employees": {"icon": "📋", "text": "عرض كل الموظفين"},
    "search_employee": {"icon": "🔍", "text": "بحث عن موظف"},
}


def get_employees_menu_keyboard() -> InlineKeyboardMarkup:
    """
    تقوم ببناء وإرجاع لوحة المفاتيح الخاصة بقائمة شؤون الموظفين.
    """
    keyboard = []
    for key, details in EMPLOYEES_MENU_STRUCTURE.items():
        button = InlineKeyboardButton(
            f"{details['icon']} {details['text']}",
            callback_data=f"employees:{key}",  # e.g., "employees:add_employee"
        )
        keyboard.append([button])

    # إضافة زر الرجوع للقائمة الرئيسية
    back_button = InlineKeyboardButton("🔙 رجوع", callback_data="menu:main_back")
    keyboard.append([back_button])

    return InlineKeyboardMarkup(keyboard)


async def show_employees_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    تعرض القائمة الفرعية الخاصة بشؤون الموظفين.
    """
    query = update.callback_query
    await query.answer()

    reply_markup = get_employees_menu_keyboard()
    await query.edit_message_text(
        text="اختر من قائمة شؤون الموظفين:", reply_markup=reply_markup
    )
