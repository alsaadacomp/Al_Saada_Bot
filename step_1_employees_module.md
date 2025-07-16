# Step 1: Employees Module Implementation

**Date:** 2025-07-16

## 1. Overview

This document outlines the first step in the implementation of the Alsaada Bot, focusing on the "Employees" module. This work aligns with the project's documented plan to build the bot feature by feature.

## 2. Changes Implemented

### a. Restored the Main Menu

The `/start` command has been updated to display the main menu with all the planned features, as defined in the project's documentation. This provides a clear user interface and sets the stage for future development.

### b. Database Setup for Employees

The `src/alsaada_bot/database.py` file has been created and configured with the following:

*   **SQLAlchemy Engine:** The file now contains the SQLAlchemy engine, configured to use a local SQLite database (`alsaada_bot.db`).
*   **Employee Model:** An `Employee` ORM model has been defined, mirroring the structure specified in the `db.csv` file. This model includes fields for `id`, `name`, `national_id`, `job_title`, and other relevant employee information.
*   **Database Initialization:** A function `init_db()` has been included to create the database and the `employees` table.

## 3. How to Run

1.  **Initialize the database:** Before running the bot for the first time, you need to create the database tables. Run the following command from your terminal:

    ```
    python src/alsaada_bot/database.py
    ```

2.  **Run the bot:** Start the bot as usual:

    ```
    python main.py
    ```

## 4. Next Steps

The foundation for the Employees module is now in place. The next steps will involve creating handlers to:

*   Add new employees.
*   View a list of employees.
*   Edit employee information.
*   Delete employees.
