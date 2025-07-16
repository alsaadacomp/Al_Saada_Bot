import logging
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes
from src.alsaada_bot.database import SessionLocal, Employee


async def start_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the employee upload process."""
    await update.message.reply_text(
        "لرفع بيانات الموظفين، يرجى إرسال ملف Excel يحتوي على الأعمدة التالية: "
        "الاسم الكامل, اللقب, تاريخ الميلاد, رقم الهوية الوطنية, الحالة الاجتماعية, "
        "العنوان الحالي, العنوان الدائم, تاريخ التعيين, المسمى الوظيفي, القسم, "
        "نوع الراتب, مبلغ الراتب, رخصة القيادة, رقم الجوال 1, رقم الجوال 2, "
        "رقم التحويل النقدي 1, نوع التحويل النقدي 1, رقم التحويل النقدي 2, "
        "نوع التحويل النقدي 2, ملاحظات إضافية, حالة التوظيف, رقم الملف / كود الوظيفة, "
        "اسم جهة الاتصال للطوارئ, رقم جهة الاتصال للطوارئ, المؤهل العلمي"
    )
    await update.message.reply_document(document=open("employees_template.xlsx", "rb"))


async def handle_employee_upload(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handles the uploaded Excel file."""
    file = await context.bot.get_file(update.message.document.file_id)
    file_path = await file.download_to_drive()

    try:
        df = pd.read_excel(file_path)
        session = SessionLocal()
        added_count = 0
        updated_count = 0

        for _, row in df.iterrows():
            employee_data = row.to_dict()
            national_id = employee_data.get("national_id_number")

            if national_id:
                existing_employee = (
                    session.query(Employee)
                    .filter_by(national_id_number=str(national_id))
                    .first()
                )
                if existing_employee:
                    for key, value in employee_data.items():
                        setattr(existing_employee, key, value)
                    updated_count += 1
                else:
                    new_employee = Employee(**employee_data)
                    session.add(new_employee)
                    added_count += 1
            else:
                # Handle rows with no national_id if necessary
                pass

        session.commit()
        session.close()

        await update.message.reply_text(
            f"تم الرفع بنجاح!\nتمت إضافة: {added_count} موظف جديد.\nتم تحديث: {updated_count} موظف موجود."
        )

    except Exception as e:
        logging.error(f"Error processing employee upload: {e}")
        await update.message.reply_text(
            "حدث خطأ أثناء معالجة الملف. يرجى التأكد من أنه بالصيغة الصحيحة."
        )
