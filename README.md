# Budget Budget 

A web-based Expense Tracker built using Flask, SQLite, SQLAlchemy, Bootstrap, HTML, and CSS.



## Features

- User Registration & Login
- Secure Password Hashing
- Add Expenses
- Edit Expenses
- Delete Expenses
- Search Expenses
- Expense Analytics
- Budget Management
- User-specific Data Storage
- Responsive Dashboard

## Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite

### Frontend
- HTML
- CSS
- Bootstrap 5Expense-Tracker/
│
├── app.py
│
├── instance/
│   └── expenses.db
│
├── static/
│   ├── style.css
│   └── images/
│       └── logo.png
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── add_expense.html
│   ├── expenses.html
│   ├── edit_expense.html
│   ├── analytics.html
│   ├── budget.html
│   ├── login.html
│   └── register.html
│
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── dashboard.png
    ├── expenses.png
    ├── analytics.png
    ├── budget.png
    ├── login.png
    └── register.png

## Installation

### Clone Repository

```bash
git clone <your-github-repository-link>
```

### Navigate to Project Folder

```bash
cd Expense-Tracker
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Environment

Windows:

```bash
env\Scripts\activate
```

### Install Dependencies

```bash
pip install flask
pip install flask_sqlalchemy
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Database

This project uses SQLite database.

Database file:

```text
instance/expenses.db
```

## Future Improvements

- User Authentication
- Monthly Reports
- Expense Charts
- Export to Excel/PDF
- Multi-user Support

