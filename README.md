# CampusDesk

CampusDesk is a Python-based Student Academic Management System created for the flipped-course project.

## Features

- Admin login
- Student CRUD operations
- Email, phone and student-ID validation using Regular Expressions
- Marks entry and automatic grade calculation
- Attendance calculation
- SQLite database storage
- CSV and JSON export
- HTML academic report generation
- Analytics dashboard
- Multithreaded report generation
- OOP design with inheritance and abstract classes
- Optional MySQL/ODBC demonstration

## Demo Login

Username: `admin`
Password: `admin123`

## Requirements

Python 3.10+ is recommended.

Optional MySQL support:
```bash
pip install mysql-connector-python
```

## Run

```bash
python main.py
```

## Test

```bash
python -m unittest discover tests
```

## Project Structure

- `models/` - OOP model classes
- `database/` - database layer
- `gui/` - Tkinter user interface
- `utils/` - validation, files and reports
- `tests/` - unit tests
- `reports/` - generated CSV, JSON and HTML reports

## Database

The default version uses SQLite so the project can be executed immediately without installing a database server. `database/mysql_connection.py` demonstrates how the same project can connect to MySQL using Python's MySQL connector.

## Academic Concepts Demonstrated

Unit 1: Python syntax, data types, operators, conditions and functions.

Unit 2: functions, exceptions, modules, collections and regular expressions.

Unit 3: classes, objects, inheritance, polymorphism and abstract classes.

Unit 4: file handling, directories, metadata, database programming and MySQL connectivity.

Unit 5: Tkinter GUI, event-driven programming, widgets, multithreading and HTML report generation.
