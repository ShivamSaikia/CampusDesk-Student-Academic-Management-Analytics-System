"""
Optional MySQL/ODBC demonstration for Unit 4.

Install:
    pip install mysql-connector-python

Then configure credentials in config.py.

This file is not required for the default SQLite version.
"""
from config import MYSQL_CONFIG

def get_mysql_connection():
    import mysql.connector
    return mysql.connector.connect(**MYSQL_CONFIG)
