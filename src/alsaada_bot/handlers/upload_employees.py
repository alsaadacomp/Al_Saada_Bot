import logging
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes
from src.alsaada_bot.database import SessionLocal, Employee

async def start_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the employee upload process."""
    await update.message.reply_text(
        "To upload employees, please send an Excel file with the following columns: "
        "full_name_ar, nickname_ar, date_of_birth, national_id_number, marital_status_ar, "
        "current_address_ar, permanent_address_ar, date_of_hire, job_title_ar, department_ar, "
        "salary_type_ar, salary_amount, drivers_license_ar, mobile_number_1, mobile_number_2, "
        "cash_transfer_number_1, cash_transfer_type_1_ar, cash_transfer_number_2, "
        "cash_transfer_type_2_ar, additional_notes_ar, employment_status_ar, file_number_ar, "
        "emergency_contact_name_ar, emergency_contact_number, educational_qualification_ar"
    )
    await update.message.reply_document(document=open("employees_template.xlsx", "rb"))

async def handle_employee_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
                existing_employee = session.query(Employee).filter_by(national_id_number=str(national_id)).first()
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
            f"Upload successful!\nAdded: {added_count} new employees.\nUpdated: {updated_count} existing employees."
        )

    except Exception as e:
        logging.error(f"Error processing employee upload: {e}")
        await update.message.reply_text("An error occurred while processing the file. Please ensure it is in the correct format.")
