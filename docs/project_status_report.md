
# Project Status Report: Alsaada_Bot

**Date:** 2025-07-16

## 1. Project Overview

**Project Name:** Alsaada_Bot

**Purpose:** A Telegram bot for "Alsaada Contracting," designed to manage various business operations.

**Current Status:** The project is in the initial development phase. The basic bot skeleton is in place, but the core features are not yet implemented.

## 2. Core Functionality

*   **Telegram Bot:** The project utilizes the `python-telegram-bot` library to create a Telegram bot.
*   **`/start` command:** Greets users with a welcome message and a main menu.
*   **Main Menu:** The main menu provides buttons for various business functions. Currently, all buttons lead to an "under development" message.
    *   Employees
    *   Salaries and Advances
    *   Attendance and Leave
    *   Expenses
    *   Suppliers
    *   Asset Inventory
    *   Maintenance
    *   Daily Operations
    *   Contractor Accounts
    *   Rented Equipment
    *   Notes and Tasks

## 3. Project Structure & Files

The project follows a standard Python project structure.

```
F:/_Alsaada_Telegram_Bot/Alsaada_Bot/
├───.editorconfig
├───.gitignore
├───AUTHORS.rst
├───CODE_OF_CONDUCT.rst
├───CONTRIBUTING.rst
├───HISTORY.rst
├───main.py
├───Makefile
├───MANIFEST.in
├───pyproject.toml
├───README.rst
├───requirements_dev.txt
├───requirements.txt
├───.git/...
├───.github/
│   ├───ISSUE_TEMPLATE.md
│   └───workflows/
│       └───test.yml
├───.My_doc/
│   ├───db.csv
│   ├───أفضل_هيكلية_تطوير_تدريجي_وتغليف_بوت_erp_مقاولات.md
│   ├───التصور_والخطة_التنفيذية_الكاملة_لمشروع_بوت_المقاولات.md
│   ├───الجدول_النهائي_المختصر_لكل_وظائف_مشروع_المقاولات.md
│   ├───تقرير مرحلي عن مشروع بوت Al_Saada_Bot16-7-2025.docx
│   └───خارطة الطريق التنفيذية المفصلة لمشروع بوت المقاولات.docx
├───docs/
│   ├───authors.rst
│   ├───contributing.rst
│   ├───history.rst
│   ├───index.rst
│   ├───installation.rst
│   ├───make.bat
│   ├───readme.rst
│   └───usage.rst
├───src/
│   ├───alsaada_bot/
│   │   ├───__init__.py
│   │   ├───alsaada_bot.py
│   │   ├───bot.py
│   │   ├───utils.py
│   │   └───__pycache__/
│   └───alsaada_bot.egg-info/
├───tests/
│   ├───__init__.py
│   └───test_alsaada_bot.py
└───venv/
    ├───Include/...
    ├───Lib/...
    └───Scripts/...
```

### Key Files:

*   **`main.py`**: The main entry point for running the bot.
*   **`src/alsaada_bot/`**: The main source code directory.
*   **`.My_doc/`**: Contains project planning documents in Arabic.
*   **`requirements.txt`**: Lists the project's Python dependencies.

## 4. Dependencies

*   **Core:** `python-telegram-bot`, `python-dotenv`, `SQLAlchemy`, `alembic`
*   **Data Handling:** `pandas`, `openpyxl`, `reportlab`
*   **Task Scheduling:** `APScheduler`
*   **Google Integration:** `gspread`, `pydrive`
*   **Image Processing:** `Pillow`
*   **Development/Testing:** `pytest`, `flake8`, `black`

## 5. Next Steps & Recommendations

The project has a solid foundation. The next logical steps are to begin implementing the functionality for each of the main menu items, likely involving database integration as suggested by the presence of `SQLAlchemy` and a `db.csv` file.
