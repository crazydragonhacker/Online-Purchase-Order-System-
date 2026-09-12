"""
MySQL data-access helper.

Replaces the original cx_Oracle connection with mysql-connector-python.
All SQL in this project uses parameterized queries (never raw string
concatenation) to avoid SQL injection, which the original app was
vulnerable to.
"""
import mysql.connector
from mysql.connector import Error as MySQLError

from .config import DB_CONFIG


def get_connection():
    """Open a new MySQL connection using settings from the environment.

    Raises ConnectionError with a friendly message if the database is
    unreachable, so the GUI can show a message box instead of crashing.
    """
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except MySQLError as exc:
        raise ConnectionError(
            f"Could not connect to MySQL database '{DB_CONFIG['database']}' "
            f"at {DB_CONFIG['host']}:{DB_CONFIG['port']}: {exc}"
        ) from exc


def insert_customer(conn, first_name, last_name, email, street1, street2, city, state):
    sql = (
        "INSERT INTO CUSTOMER (first_name, last_name, email, street1, street2, city, state) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    cursor = conn.cursor()
    cursor.execute(sql, (first_name, last_name, email, street1, street2, city, state))
    conn.commit()
    customer_id = cursor.lastrowid
    cursor.close()
    return customer_id


def insert_product_order(conn, order_id, pid):
    sql = "INSERT INTO PRODUCTORDER (order_id, pid) VALUES (%s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, (order_id, pid))
    cursor.close()


def insert_payment(conn, order_id, amount, pay_mode):
    sql = "INSERT INTO PAYMENT (order_id, amount, pay_mode) VALUES (%s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, (order_id, amount, pay_mode))
    conn.commit()
    cursor.close()
