from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database Setup ---
# Using SQLite for simplicity and portability.
DATABASE_URL = "sqlite:///./alsaada_bot.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Enums for Dropdown Lists (as per user requirements) ---
# These provide consistency at the application level.
MARITAL_STATUS_OPTIONS = ["Single", "Married", "Divorced", "Widowed"]
SALARY_TYPE_OPTIONS = ["Daily", "Monthly", "Piecework"]
LICENSE_TYPE_OPTIONS = ["None", "First Class", "Second Class", "Third Class", "Private"]
TRANSFER_TYPE_OPTIONS = ["Wallet", "Instapay"]
EMPLOYMENT_STATUS_OPTIONS = [
    "Current Employee",
    "Suspended",
    "Terminated",
    "Deceased",
    "Other",
]


# --- ORM Model for the Employee Table ---
class Employee(Base):
    __tablename__ = "employees"

    # Core Identification
    id = Column(Integer, primary_key=True, index=True)
    worker_code = Column(
        String, unique=True, index=True, nullable=True
    )  # Auto-generated
    full_name_ar = Column(String, nullable=False)
    nickname_ar = Column(String, nullable=True)
    profile_photo_path = Column(String, nullable=True)  # Stores path to image

    # Personal Information
    date_of_birth = Column(Date, nullable=True)
    national_id_number = Column(String, unique=True, nullable=True)
    marital_status_ar = Column(String, nullable=True)
    current_address_ar = Column(String(200), nullable=True)
    permanent_address_ar = Column(String(200), nullable=True)
    educational_qualification_ar = Column(String(100), nullable=True)
    national_id_image_path = Column(String, nullable=True)

    # Employment Details
    date_of_hire = Column(Date, nullable=True)
    job_title_ar = Column(String(100), nullable=True)
    department_ar = Column(String, nullable=True)
    employment_status_ar = Column(String, default="Current Employee")
    file_number_ar = Column(String, unique=True, nullable=True)

    # Financial Information
    salary_type_ar = Column(String, nullable=True)
    salary_amount = Column(Float, nullable=True)

    # Contact and Emergency
    mobile_number_1 = Column(String(11), nullable=True)
    mobile_number_2 = Column(String(11), nullable=True)
    emergency_contact_name_ar = Column(String(50), nullable=True)
    emergency_contact_number = Column(String(11), nullable=True)

    # Wallet / Instapay
    cash_transfer_number_1 = Column(String(11), nullable=True)
    cash_transfer_type_1_ar = Column(String, nullable=True)
    cash_transfer_number_2 = Column(String(11), nullable=True)
    cash_transfer_type_2_ar = Column(String, nullable=True)

    # Other
    drivers_license_ar = Column(String, nullable=True)
    additional_notes_ar = Column(String(300), nullable=True)


# --- Database Initialization ---
def init_db():
    """Create the database tables based on the models defined."""
    print("Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
