import pandas as pd

df = pd.DataFrame(columns=[
    "full_name_ar", "nickname_ar", "date_of_birth", "national_id_number",
    "marital_status_ar", "current_address_ar", "permanent_address_ar",
    "date_of_hire", "job_title_ar", "department_ar", "salary_type_ar",
    "salary_amount", "drivers_license_ar", "mobile_number_1", "mobile_number_2",
    "cash_transfer_number_1", "cash_transfer_type_1_ar", "cash_transfer_number_2",
    "cash_transfer_type_2_ar", "additional_notes_ar", "employment_status_ar",
    "file_number_ar", "emergency_contact_name_ar", "emergency_contact_number",
    "educational_qualification_ar"
])

df.to_excel("employees_template.xlsx", index=False)
