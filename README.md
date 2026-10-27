# English Session Attendance Tracker

A lightweight attendance management tool built with **Python** and **PostgreSQL** to manage students and track attendance in English teaching sessions.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Project Status](#project-status)
- [Getting Started](#getting-started)
- [Author](#author)

## Features

- **Student Management** — Add students and manage student records.
- **Input Validation** — Validate student names and grade levels.
- **Grade Classification** — Support Fundamentals and Grades 1–7.
- **Attendance Tracking** — Planned.
- **Attendance History** — Planned.

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

## Project Structure

```text
student_management/
├── database/
│   ├── connection.py
│   └── schema.sql
├── students/
│   └── operations.py
├── utils/
│   ├── constants.py
│   └── validators.py
├── main.py
├── .env
├── .gitignore
└── README.md
```

## Project Status

**In Development**

The PostgreSQL schema and database connection are configured. Student creation and input validation have been implemented and tested. Attendance tracking and attendance history are planned for future development.

## Getting Started

### Prerequisites

- Python
- PostgreSQL

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/theyoussefmoussa/english_sessions_tracker.git
   cd student_management
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
python3 -m pip install -r requirements.txt
```

4. Create a `.env` file in the project root and configure your database credentials:

   ```env
   DB_NAME=your_database
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Configure PostgreSQL and apply the database schema using `database/schema.sql`.

6. Run the application:

   ```bash
   python3 main.py
   ```

## Author

**Youssef Moussa**

- LinkedIn: [Connect with me](https://linkedin.com/in/theyoussefmoussa)
- Portfolio: [Visit my portfolio](https://theyoussefmoussa.github.io)

---

*Built to simplify English session attendance management through Python and PostgreSQL.*